#!/usr/bin/env python3
"""Protect explicitly designated skills against silent upstream or local drift."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any
from urllib.parse import urlsplit


VERSION = 1
MANIFEST_KEY = "protected_upstream"
UPSTREAM_REF_ROOT = "refs/skillshare-protected"
SEVERITY = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


class Blocked(RuntimeError):
    pass


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(content: bytes) -> str:
    try:
        content.decode("utf-8")
    except UnicodeDecodeError:
        normalized = content
    else:
        normalized = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return "sha256:" + hashlib.sha256(normalized).hexdigest()


def directory_hash(file_hashes: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for name, value in sorted(file_hashes.items()):
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(value.encode("ascii"))
        digest.update(b"\n")
    return "sha256:" + digest.hexdigest()


def command(args: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(args, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True)
    except FileNotFoundError as exc:
        raise Blocked(f"Required command is unavailable: {args[0]}") from exc
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise Blocked(f"Command failed ({result.returncode}): {' '.join(args)}\n{detail}")
    return result


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return command(["git", *args], cwd=root, check=check)


def load_metadata(root: Path) -> dict[str, Any]:
    path = root / ".metadata.json"
    try:
        metadata = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Blocked(f"Cannot read {path}: {exc}") from exc
    if not isinstance(metadata, dict) or metadata.get("version") != 1:
        raise Blocked("Unsupported .metadata.json format")
    return metadata


def protected(metadata: dict[str, Any], *, required: bool = True) -> dict[str, Any]:
    manifest = metadata.get(MANIFEST_KEY)
    if manifest is None and not required:
        return {"version": VERSION, "skills": {}}
    if not isinstance(manifest, dict) or manifest.get("version") != VERSION or not isinstance(manifest.get("skills"), dict):
        raise Blocked(".metadata.json has no valid protected_upstream manifest")
    skills = manifest["skills"]
    for name, entry in skills.items():
        if not isinstance(name, str) or not isinstance(entry, dict):
            raise Blocked("Invalid protected_upstream skill entry")
        if name in (".", "..", ".git", ".hg", ".svn") or not re.fullmatch(r"[A-Za-z0-9._-]+", name) or windows_reserved(name):
            raise Blocked(f"Unsafe protected skill name: {name}")
        for key in ("source", "branch", "source_path", "commit", "tree_hash", "directory_hash", "file_hashes"):
            if key not in entry:
                raise Blocked(f"Protected skill {name} is missing {key}")
        if not isinstance(entry["source"], str) or not valid_source(entry["source"]) or not isinstance(entry["branch"], str) or not entry["branch"]:
            raise Blocked(f"Protected skill {name} has invalid source identity")
        if not isinstance(entry["source_path"], str):
            raise Blocked(f"Protected skill {name} has an invalid source path")
        if not isinstance(entry["commit"], str) or not re.fullmatch(r"[0-9a-f]{40}", entry["commit"]):
            raise Blocked(f"Protected skill {name} has an invalid adopted commit")
        source_path = safe_rel(entry["source_path"])
        source_root = entry.get("source_root", "skills")
        if not isinstance(source_root, str):
            raise Blocked(f"Protected skill {name} has an invalid source root")
        source_root = safe_rel(source_root)
        if not source_path.startswith(source_root + "/"):
            raise Blocked(f"Protected skill {name} source path is outside its source root")
        if not isinstance(entry["tree_hash"], str) or not re.fullmatch(r"sha1:[0-9a-f]{40}", entry["tree_hash"]):
            raise Blocked(f"Protected skill {name} has an invalid source tree hash")
        if not isinstance(entry["file_hashes"], dict):
            raise Blocked(f"Protected skill {name} has invalid file_hashes")
        for file_name, value in entry["file_hashes"].items():
            if not isinstance(file_name, str):
                raise Blocked(f"Protected skill {name} has a non-text file path")
            safe_rel(file_name)
            if not isinstance(value, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", value):
                raise Blocked(f"Protected skill {name} has an invalid file hash for {file_name}")
        if not isinstance(entry["directory_hash"], str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", entry["directory_hash"]):
            raise Blocked(f"Protected skill {name} has an invalid directory hash")
        if directory_hash(entry["file_hashes"]) != entry["directory_hash"]:
            raise Blocked(f"Protected skill {name} has an inconsistent directory hash")
        approved = entry.get("approved_changes", [])
        if not isinstance(approved, list) or any(not isinstance(item, dict) or not re.fullmatch(r"[0-9a-f]{40}", str(item.get("commit", ""))) or not str(item.get("reason", "")).strip() for item in approved):
            raise Blocked(f"Protected skill {name} has invalid approved_changes")
        exception = entry.get("local_exception")
        if exception is not None and (not isinstance(exception, dict) or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(exception.get("directory_hash", ""))) or not str(exception.get("reason", "")).strip()):
            raise Blocked(f"Protected skill {name} has an invalid local exception")
    if not isinstance(manifest.get("retired", []), list):
        raise Blocked("protected_upstream.retired must be a list")
    return manifest


def safe_rel(name: str) -> str:
    path = PurePosixPath(name)
    if "\\" in name or path.is_absolute() or not path.parts or any(part in ("", ".", "..") or windows_reserved(part) or re.search(r'[<>:"|?*]', part) or part.endswith((".", " ")) for part in path.parts):
        raise Blocked(f"Unsafe upstream file path: {name}")
    return path.as_posix()


def windows_reserved(name: str) -> bool:
    stem = name.split(".", 1)[0].upper()
    return stem in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def validate_windows_paths(names: set[str]) -> None:
    """Reject source paths that collide or change spelling on Windows."""
    spellings: dict[tuple[tuple[str, ...], str], str] = {}
    file_paths: set[tuple[str, ...]] = set()
    for name in sorted(names):
        parts = PurePosixPath(name).parts
        folded = tuple(part.casefold() for part in parts)
        for index, part in enumerate(parts):
            parent = folded[:index]
            key = (parent, part.casefold())
            previous = spellings.get(key)
            if previous is not None and previous != part:
                raise Blocked(f"Upstream paths differ only by Windows-insensitive casing: {name}")
            spellings[key] = part
        if folded in file_paths:
            raise Blocked(f"Upstream paths collide on Windows: {name}")
        if any(folded[:index] in file_paths for index in range(1, len(folded))):
            raise Blocked(f"An upstream file is also a parent directory on Windows: {name}")
        if any(existing[:len(folded)] == folded for existing in file_paths):
            raise Blocked(f"An upstream file conflicts with a child path on Windows: {name}")
        file_paths.add(folded)


def valid_source(url: str) -> bool:
    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname
    except ValueError:
        return False
    return parsed.scheme == "https" and bool(hostname) and parsed.username is None and parsed.password is None and not parsed.query and not parsed.fragment


def local_snapshot(path: Path) -> dict[str, str]:
    if not path.is_dir():
        raise Blocked(f"Protected directory is missing: {path}")
    files: dict[str, str] = {}
    for current, dirs, names in os.walk(path, followlinks=False):
        base = Path(current)
        for dirname in list(dirs):
            if (base / dirname).is_symlink():
                raise Blocked(f"Symlink in protected directory: {base / dirname}")
        for filename in names:
            file_path = base / filename
            if file_path.is_symlink():
                raise Blocked(f"Symlink in protected directory: {file_path}")
            relative = file_path.relative_to(path).as_posix()
            files[relative] = sha256_bytes(file_path.read_bytes())
    return files


def source_files(root: Path, commit: str, source_path: str) -> tuple[dict[str, bytes], str]:
    source_path = safe_rel(source_path)
    result = subprocess.run(["git", "ls-tree", "-r", "-z", commit, "--", source_path], cwd=root, capture_output=True, check=False)
    if result.returncode:
        raise Blocked(f"Could not read upstream tree {commit}:{source_path}")
    files: dict[str, bytes] = {}
    prefix = source_path.rstrip("/") + "/"
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        try:
            header, raw_name = record.split(b"\t", 1)
            mode, kind, oid = header.decode("ascii").split()
            name = raw_name.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise Blocked("Could not parse upstream Git tree") from exc
        if kind == "tree":
            continue
        if kind != "blob" or mode not in ("100644", "100755"):
            raise Blocked(f"Unsupported non-regular object in upstream skill: {name}")
        if not name.startswith(prefix):
            continue
        relative = safe_rel(name[len(prefix):])
        raw = subprocess.run(["git", "cat-file", "blob", oid], cwd=root, capture_output=True, check=False)
        if raw.returncode:
            raise Blocked(f"Could not read upstream blob {oid}")
        files[relative] = raw.stdout
    validate_windows_paths(set(files))
    tree_result = git(root, "rev-parse", "--verify", f"{commit}:{source_path}", check=False)
    if tree_result.returncode:
        raise Blocked(f"Upstream skill directory is missing at {commit}: {source_path}")
    return files, "sha1:" + tree_result.stdout.strip()


def source_skill_paths(root: Path, commit: str, source_root: str = "skills") -> dict[str, str]:
    source_root = safe_rel(source_root)
    raw = subprocess.run(["git", "ls-tree", "-r", "-z", "--name-only", commit, "--", source_root], cwd=root, capture_output=True, check=False)
    if raw.returncode:
        raise Blocked(f"Could not list upstream skills under {source_root} at {commit}")
    found: dict[str, str] = {}
    prefix = source_root.rstrip("/") + "/"
    for item in raw.stdout.split(b"\0"):
        if not item:
            continue
        try:
            path = item.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Blocked("Upstream skill path is not valid UTF-8") from exc
        if not path.startswith(prefix):
            continue
        if not path.endswith("/SKILL.md"):
            continue
        directory = path.rsplit("/", 1)[0]
        name = directory.rsplit("/", 1)[-1]
        if name in found and found[name] != directory:
            raise Blocked(f"Upstream has more than one skill named {name}")
        found[name] = directory
    return found


def fetch(root: Path, url: str, branch: str) -> str:
    if not valid_source(url):
        raise Blocked(f"Upstream source must be an HTTPS URL without embedded credentials or query data: {url}")
    if git(root, "check-ref-format", "--branch", branch, check=False).returncode:
        raise Blocked(f"Invalid upstream branch name: {branch}")
    slug = hashlib.sha256(f"{url}\0{branch}".encode("utf-8")).hexdigest()[:16]
    ref = f"{UPSTREAM_REF_ROOT}/{slug}/{branch}"
    command(["git", "fetch", "--quiet", "--no-tags", "--force", url, f"+refs/heads/{branch}:{ref}"], cwd=root)
    return git(root, "rev-parse", "--verify", f"{ref}^{{commit}}").stdout.strip()


def write_snapshot(destination: Path, files: dict[str, bytes]) -> None:
    for relative, content in files.items():
        target = destination.joinpath(*PurePosixPath(safe_rel(relative)).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)


def audit_snapshot(name: str, files: dict[str, bytes], parent: Path) -> None:
    audit_dir = parent / name
    if audit_dir.exists():
        shutil.rmtree(audit_dir)
    write_snapshot(audit_dir, files)
    result = command(["skillshare", "audit", str(audit_dir), "--threshold", "critical", "--no-tui", "--format", "json"], cwd=parent, check=False)
    if result.returncode:
        raise Blocked(f"SkillShare audit failed for {name}: {result.stderr.strip() or result.stdout.strip()}")
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise Blocked(f"SkillShare returned unreadable audit output for {name}") from exc
    summary = report.get("summary", {})
    if summary.get("scanErrors", 0):
        raise Blocked(f"SkillShare could not fully scan {name}")
    for item in report.get("results", []):
        if item.get("auditableBytes", 0) != item.get("totalBytes", 0):
            raise Blocked(f"SkillShare could not audit every byte in {name}")
        critical = [finding for finding in (item.get("findings") or []) if SEVERITY.get(str(finding.get("severity", "")).upper(), 0) >= SEVERITY["CRITICAL"]]
        if critical:
            lines = "; ".join(f"{f.get('severity')} {f.get('file')}:{f.get('line')} {f.get('message')}" for f in critical)
            raise Blocked(f"Critical SkillShare findings in {name}: {lines}")
    if not report.get("results"):
        raise Blocked(f"SkillShare did not audit {name}")


def file_map(files: dict[str, bytes]) -> dict[str, str]:
    return {name: sha256_bytes(content) for name, content in sorted(files.items())}


def skill_entry(url: str, branch: str, source_path: str, commit: str, tree_hash: str, files: dict[str, bytes], source_root: str = "skills") -> dict[str, Any]:
    hashes = file_map(files)
    entry = {
        "source": url,
        "branch": branch,
        "source_path": source_path,
        "commit": commit,
        "tree_hash": tree_hash,
        "directory_hash": directory_hash(hashes),
        "file_hashes": hashes,
        "approved_changes": [],
    }
    if source_root != "skills":
        entry["source_root"] = safe_rel(source_root)
    return entry


def git_metadata_path(root: Path, name: str) -> Path:
    value = git(root, "rev-parse", "--git-path", name).stdout.strip()
    path = Path(value)
    return path if path.is_absolute() else root / path


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def write_metadata(root: Path, metadata: dict[str, Any]) -> None:
    write_json(root / ".metadata.json", metadata)


def receipt(root: Path, category: str, details: dict[str, Any]) -> Path:
    folder = git_metadata_path(root, "protected-upstream/receipts")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = folder / f"{stamp}-{category}.json"
    write_json(path, {"created_at": now(), "category": category, **details})
    return path


def check_canonical(root: Path, manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for name, entry in sorted(manifest["skills"].items()):
        try:
            actual = local_snapshot(root / name)
        except Blocked as exc:
            failures.append(str(exc))
            continue
        actual_hash = directory_hash(actual)
        expected = entry["directory_hash"]
        exception = entry.get("local_exception")
        if actual_hash != expected:
            if not isinstance(exception, dict) or exception.get("directory_hash") != actual_hash or not exception.get("reason"):
                failures.append(f"{name}: canonical drift: expected {expected}, found {actual_hash}")
            else:
                print(f"EXCEPTION {name}: {exception['reason']}")
    return failures


def target_manages(target: dict[str, Any], name: str) -> bool:
    includes = target.get("include") or []
    excludes = target.get("exclude") or []
    if includes and not any(fnmatch.fnmatchcase(name, pattern) for pattern in includes):
        return False
    return not any(fnmatch.fnmatchcase(name, pattern) for pattern in excludes)


def check_projections(root: Path, manifest: dict[str, Any]) -> list[str]:
    result = command(["skillshare", "target", "list", "--json"], cwd=root)
    try:
        targets = json.loads(result.stdout).get("targets", [])
    except json.JSONDecodeError as exc:
        raise Blocked("Could not read SkillShare target list") from exc
    failures: list[str] = []
    for target in targets:
        target_root = Path(target["path"])
        naming = target.get("targetNaming", "flat")
        if naming != "flat":
            failures.append(f"{target.get('name')}: unsupported projection naming {naming}; verify the mapping before maintenance")
            continue
        for name, entry in sorted(manifest["skills"].items()):
            if not target_manages(target, name):
                continue
            source = root / name
            destination = target_root / name
            if not destination.exists():
                failures.append(f"{target.get('name')}/{name}: managed projection is missing")
                continue
            try:
                if os.path.samefile(source, destination):
                    actual_hash = directory_hash(local_snapshot(source))
                else:
                    actual_hash = directory_hash(local_snapshot(destination))
            except (OSError, Blocked) as exc:
                failures.append(f"{target.get('name')}/{name}: {exc}")
                continue
            expected = (entry.get("local_exception") or {}).get("directory_hash", entry["directory_hash"])
            if actual_hash != expected:
                failures.append(f"{target.get('name')}/{name}: projection drift: expected {expected}, found {actual_hash}")
    return failures


def cmd_check(root: Path, *, record_failures: bool = True) -> None:
    metadata = load_metadata(root)
    manifest = protected(metadata)
    failures = check_canonical(root, manifest)
    if not failures:
        failures.extend(check_projections(root, manifest))
    if failures:
        receipt_path = receipt(root, "blocked-check", {"failures": failures}) if record_failures else None
        details = "\n".join(f"- {item}" for item in failures)
        if receipt_path:
            details += f"\nReceipt: {receipt_path}"
        raise Blocked(details)
    print(f"Protected-skill check passed: {len(manifest['skills'])} canonical directories and configured projections match.")


def cmd_adopt(root: Path, args: argparse.Namespace) -> None:
    metadata = load_metadata(root)
    manifest = protected(metadata, required=False)
    source_url = args.source_url
    branch = args.branch
    if not valid_source(source_url):
        raise Blocked("Upstream source must be an HTTPS URL without embedded credentials or query data")
    tip = fetch(root, source_url, branch)
    commit = tip
    if args.commit:
        if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
            raise Blocked("An adopted historical commit must be a full 40-character SHA")
        resolved = git(root, "rev-parse", "--verify", f"{args.commit}^{{commit}}", check=False)
        if resolved.returncode or resolved.stdout.strip() != args.commit:
            raise Blocked(f"Adopted commit is unavailable: {args.commit}")
        if not upstream_is_ancestor(root, args.commit, tip):
            raise Blocked(f"Adopted commit {args.commit} is not an ancestor of fetched {branch} tip {tip}")
        commit = args.commit
    source_root = safe_rel(args.source_root)
    paths = source_skill_paths(root, commit, source_root)
    new_entries = dict(manifest["skills"])
    with tempfile.TemporaryDirectory(prefix="protected-skill-audit-") as temporary:
        temp_root = Path(temporary)
        for name in args.skills:
            if name in new_entries:
                raise Blocked(f"Skill is already designated: {name}")
            source_path = paths.get(name)
            if source_path is None:
                raise Blocked(f"Upstream skill not found: {name}")
            files, tree_hash = source_files(root, commit, source_path)
            hashes = file_map(files)
            local = local_snapshot(root / name)
            if local != hashes:
                raise Blocked(f"Cannot adopt {name}: canonical content does not match {source_url}@{commit}:{source_path}")
            audit_snapshot(name, files, temp_root)
            new_entries[name] = skill_entry(source_url, branch, source_path, commit, tree_hash, files, source_root)
            print(f"Adopted {name}: {source_path} at {commit[:12]}")
    manifest.update({"version": VERSION, "skills": dict(sorted(new_entries.items()))})
    metadata[MANIFEST_KEY] = manifest
    write_metadata(root, metadata)
    print(f"Recorded {len(args.skills)} designated skill(s) in .metadata.json.")


def approve_entry(root: Path, metadata: dict[str, Any], name: str, commit: str, reason: str) -> None:
    manifest = protected(metadata)
    entry = manifest["skills"].get(name)
    if entry is None:
        raise Blocked(f"Skill is not designated: {name}")
    candidate = fetch(root, entry["source"], entry["branch"])
    if commit not in (candidate, candidate[:12]):
        raise Blocked(f"Approval must name the fetched branch tip {candidate}")
    approvals = [item for item in entry.get("approved_changes", []) if item.get("commit") != candidate]
    approvals.append({"commit": candidate, "reason": reason.strip(), "recorded_at": now()})
    entry["approved_changes"] = approvals
    write_metadata(root, metadata)
    print(f"Recorded review approval for {name} at {candidate}.")


def cmd_exception(root: Path, args: argparse.Namespace) -> None:
    metadata = load_metadata(root)
    manifest = protected(metadata)
    entry = manifest["skills"].get(args.skill)
    if entry is None:
        raise Blocked(f"Skill is not designated: {args.skill}")
    current_hash = directory_hash(local_snapshot(root / args.skill))
    entry["local_exception"] = {"directory_hash": current_hash, "reason": args.reason.strip(), "recorded_at": now()}
    write_metadata(root, metadata)
    sync_projections(root, manifest)
    print(f"Recorded exact-hash exception for {args.skill}: {current_hash}")


def cmd_clear_exception(root: Path, args: argparse.Namespace) -> None:
    metadata = load_metadata(root)
    manifest = protected(metadata)
    entry = manifest["skills"].get(args.skill)
    if entry is None or not entry.get("local_exception"):
        raise Blocked(f"No local exception is recorded for {args.skill}")
    actual = directory_hash(local_snapshot(root / args.skill))
    if actual != entry["directory_hash"]:
        raise Blocked(f"Restore {args.skill} to its adopted upstream content before clearing its exception")
    entry.pop("local_exception", None)
    write_metadata(root, metadata)
    sync_projections(root, manifest)
    print(f"Cleared the local exception for {args.skill}.")


def cmd_preview(root: Path, skill: str | None) -> None:
    manifest = protected(load_metadata(root))
    groups: dict[tuple[str, str, str], list[tuple[str, dict[str, Any]]]] = {}
    for name, entry in manifest["skills"].items():
        if skill is None or skill == name:
            groups.setdefault((entry["source"], entry["branch"], entry.get("source_root", "skills")), []).append((name, entry))
    if skill is not None and not groups:
        raise Blocked(f"Skill is not designated: {skill}")
    for (url, branch, source_root), entries in groups.items():
        candidate = fetch(root, url, branch)
        paths = source_skill_paths(root, candidate, source_root)
        print(f"Source {url} branch {branch}, skill root {source_root}, at {candidate}")
        for name, entry in entries:
            new_path = paths.get(name)
            print(f"\n=== {name}: {entry['commit']} -> {candidate} ===")
            if new_path is None:
                print(f"Upstream skill removed. Last source path: {entry['source_path']}")
            paths_to_diff = list(dict.fromkeys([entry["source_path"], new_path or entry["source_path"]]))
            result = git(root, "diff", "--find-renames", "--no-ext-diff", "--unified=3", entry["commit"], candidate, "--", *paths_to_diff, check=False)
            if result.returncode:
                raise Blocked(f"Could not preview source changes for {name}")
            if result.stdout:
                print(result.stdout.rstrip())
            else:
                print(f"No file-content change; current source path: {new_path}")


def upstream_is_ancestor(root: Path, old_commit: str, new_commit: str) -> bool:
    return git(root, "merge-base", "--is-ancestor", old_commit, new_commit, check=False).returncode == 0


def retry_pending_push(root: Path) -> None:
    marker = git_metadata_path(root, "protected-upstream-publication-pending.json")
    if not marker.exists():
        return
    details = json.loads(marker.read_text(encoding="utf-8"))
    current = git(root, "rev-parse", "HEAD").stdout.strip()
    if current != details.get("commit"):
        raise Blocked(f"Publication is pending for {details.get('commit')}; HEAD moved to {current}. Resolve the recorded commit before another update.")
    result = git(root, "push", check=False)
    if result.returncode:
        raise Blocked(f"Publication remains pending for {current}: {result.stderr.strip() or result.stdout.strip()}")
    marker.unlink(missing_ok=True)
    print(f"Published pending protected-skill update {current[:12]}.")


def ahead_count(root: Path) -> int:
    upstream = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
    if upstream.returncode:
        return 0
    counts = git(root, "rev-list", "--left-right", "--count", f"{upstream.stdout.strip()}...HEAD").stdout.split()
    return int(counts[1])


def assert_publishable(root: Path, changed: list[str]) -> None:
    staged = git(root, "diff", "--cached", "--name-only").stdout.splitlines()
    overlap = [path for path in staged if path in changed or any(path.startswith(name + "/") for name in changed if name != ".metadata.json")]
    if overlap:
        raise Blocked(f"Unrelated staged work overlaps the protected update: {', '.join(overlap)}")
    if ahead_count(root):
        raise Blocked("The skills branch already has unpublished commits; publish or reconcile them before an automatic upstream update.")


def commit_and_push(root: Path, changed: list[str], commit_hint: str) -> None:
    assert_publishable(root, changed)
    git(root, "add", "-A", "--", *changed)
    result = git(root, "commit", "--only", "-m", f"Update protected upstream skills at {commit_hint}", "--", *changed, check=False)
    if result.returncode:
        raise Blocked(f"Could not commit the accepted upstream update: {result.stderr.strip() or result.stdout.strip()}")
    commit = git(root, "rev-parse", "HEAD").stdout.strip()
    pushed = git(root, "push", check=False)
    if pushed.returncode:
        marker = git_metadata_path(root, "protected-upstream-publication-pending.json")
        write_json(marker, {"commit": commit, "created_at": now(), "reason": pushed.stderr.strip() or pushed.stdout.strip()})
        print(f"Publication pending for {commit}; SkillShare projections are already synchronized.")
    else:
        print(f"Committed and published protected-skill update {commit[:12]}.")


def cmd_update(root: Path) -> None:
    retry_pending_push(root)
    metadata = load_metadata(root)
    manifest = protected(metadata)
    local_failures = check_canonical(root, manifest)
    if local_failures:
        path = receipt(root, "blocked-drift", {"failures": local_failures})
        raise Blocked("\n".join(local_failures) + f"\nReceipt: {path}")

    groups: dict[tuple[str, str, str], list[tuple[str, dict[str, Any]]]] = {}
    for name, entry in manifest["skills"].items():
        groups.setdefault((entry["source"], entry["branch"], entry.get("source_root", "skills")), []).append((name, entry))

    proposals: dict[str, tuple[dict[str, Any], dict[str, bytes], bool]] = {}
    retirements: dict[str, dict[str, Any]] = {}
    blocked: list[str] = []
    with tempfile.TemporaryDirectory(prefix="protected-skill-audit-") as temporary:
        temp_root = Path(temporary)
        for (url, branch, source_root), entries in groups.items():
            candidate = fetch(root, url, branch)
            paths = source_skill_paths(root, candidate, source_root)
            for name, entry in entries:
                exception = entry.get("local_exception")
                local_hash = directory_hash(local_snapshot(root / name))
                if exception and exception.get("directory_hash") == local_hash:
                    source_path = paths.get(name)
                    if source_path is None or source_path != entry["source_path"]:
                        blocked.append(f"{name}: clear its local exception and restore upstream form before handling a source removal or rename")
                        continue
                    files, tree_hash = source_files(root, candidate, source_path)
                    if file_map(files) != entry["file_hashes"]:
                        blocked.append(f"{name}: clear its local exception and restore upstream form before applying changed upstream content")
                        continue
                    updated = skill_entry(url, branch, source_path, candidate, tree_hash, files, source_root)
                    updated["local_exception"] = exception
                    proposals[name] = (updated, files, False)
                    continue
                source_path = paths.get(name)
                if source_path is None:
                    approval = next((item for item in entry.get("approved_changes", []) if item.get("commit") == candidate and item.get("reason", "").strip()), None)
                    if approval:
                        retirements[name] = {
                            "source": entry["source"],
                            "branch": entry["branch"],
                            "source_path": entry["source_path"],
                            "last_adopted_commit": entry["commit"],
                            "removed_at_commit": candidate,
                            "reason": approval["reason"],
                            "recorded_at": now(),
                            "disposition": "kept-local",
                        }
                    else:
                        blocked.append(f"{name}: upstream skill was removed; review candidate {candidate}")
                    continue
                files, tree_hash = source_files(root, candidate, source_path)
                new_hashes = file_map(files)
                removed = sorted(set(entry["file_hashes"]) - set(new_hashes))
                path_changed = source_path != entry["source_path"]
                history_rewritten = not upstream_is_ancestor(root, entry["commit"], candidate)
                needs_review = bool(removed or path_changed or history_rewritten)
                approval = next((item for item in entry.get("approved_changes", []) if item.get("commit") == candidate and item.get("reason", "").strip()), None)
                if needs_review and not approval:
                    reason = []
                    if removed:
                        reason.append("removed files: " + ", ".join(removed))
                    if path_changed:
                        reason.append(f"source path changed to {source_path}")
                    if history_rewritten:
                        reason.append("upstream history was rewritten")
                    blocked.append(f"{name}: {'; '.join(reason)}; review and approve exact commit {candidate}")
                    continue
                updated = skill_entry(url, branch, source_path, candidate, tree_hash, files, source_root)
                updated["approved_changes"] = [item for item in entry.get("approved_changes", []) if item.get("commit") != candidate]
                content_changed = updated["directory_hash"] != entry["directory_hash"]
                if content_changed:
                    audit_snapshot(name, files, temp_root)
                proposals[name] = (updated, files, content_changed)
    if blocked:
        path = receipt(root, "blocked-upstream-review", {"failures": blocked})
        raise Blocked("\n".join(blocked) + f"\nReceipt: {path}")

    changed_skills = [name for name, (_, _, changed) in proposals.items() if changed]
    metadata_changed = bool(retirements) or any(manifest["skills"][name] != updated for name, (updated, _, _) in proposals.items())
    if not changed_skills and not metadata_changed:
        print(f"Upstream branches are current: {len(manifest['skills'])} designated skills checked.")
        cmd_check(root)
        return

    changed_paths = [".metadata.json", *sorted(changed_skills)]
    assert_publishable(root, changed_paths)
    temp_root = Path(tempfile.mkdtemp(prefix="protected-skill-update-", dir=root))
    backups: dict[str, Path] = {}
    replaced: list[str] = []
    original_metadata = (root / ".metadata.json").read_bytes()
    try:
        for name in changed_skills:
            updated, files, _ = proposals[name]
            stage = temp_root / "stage" / name
            write_snapshot(stage, files)
            current = root / name
            backup = temp_root / "backup" / name
            backup.parent.mkdir(parents=True, exist_ok=True)
            os.replace(current, backup)
            backups[name] = backup
            replaced.append(name)
            os.replace(stage, current)
            manifest["skills"][name] = updated
        for name, retired in retirements.items():
            manifest["skills"].pop(name)
            manifest.setdefault("retired", []).append({"name": name, **retired})
        write_metadata(root, metadata)
    except Exception:
        for name in reversed(replaced):
            current = root / name
            if current.exists():
                shutil.rmtree(current)
            os.replace(backups[name], current)
        (root / ".metadata.json").write_bytes(original_metadata)
        raise
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

    failures = check_canonical(root, manifest)
    if failures:
        path = receipt(root, "post-update-drift", {"failures": failures})
        raise Blocked("Canonical validation failed after update:\n" + "\n".join(failures) + f"\nReceipt: {path}")
    sync_projections(root, manifest)
    print(f"Accepted updates: {', '.join(changed_skills) if changed_skills else 'source revision metadata only'}")
    if retirements:
        print("Kept source-retired skills as local skills: " + ", ".join(sorted(retirements)))
    commit_hint = max((entry["commit"] for entry, _, _ in proposals.values()), default=max((row["removed_at_commit"] for row in retirements.values()), default="unknown"))[:12]
    commit_and_push(root, changed_paths, commit_hint)


def sync_projections(root: Path, manifest: dict[str, Any]) -> None:
    sync = command(["skillshare", "sync"], cwd=root, check=False)
    if sync.returncode:
        raise Blocked(f"SkillShare sync failed: {sync.stderr.strip() or sync.stdout.strip()}")
    status = command(["skillshare", "status", "--json"], cwd=root)
    diff_stat = command(["skillshare", "diff", "--stat"], cwd=root, check=False)
    if diff_stat.returncode:
        raise Blocked(f"SkillShare diff check failed: {diff_stat.stderr.strip() or diff_stat.stdout.strip()}")
    diff_json = command(["skillshare", "diff", "--json"], cwd=root)
    try:
        diff_payload = json.loads(diff_json.stdout)
    except json.JSONDecodeError as exc:
        raise Blocked("Could not read SkillShare's structured diff") from exc
    unmanaged_changes = []
    for target in diff_payload.get("targets", []):
        for item in target.get("items", []):
            if item.get("is_sync") is False and item.get("reason") == "local only":
                continue
            unmanaged_changes.append(f"{target.get('name')}/{item.get('name')}: {item.get('action', 'difference')} ({item.get('reason', 'source-managed')})")
    failures = check_projections(root, manifest)
    failures.extend(unmanaged_changes)
    if failures:
        path = receipt(root, "projection-drift", {"failures": failures, "status": status.stdout, "diff_stat": diff_stat.stdout, "diff_json": diff_json.stdout})
        raise Blocked("Projection validation failed:\n" + "\n".join(failures) + f"\nReceipt: {path}")
    print(sync.stdout.strip())
    print(status.stdout.strip())
    print(diff_stat.stdout.strip())


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Maintain skills explicitly designated in .metadata.json.")
    result.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2], help="canonical SkillShare source root")
    sub = result.add_subparsers(dest="action", required=True)
    adopt = sub.add_parser("adopt", help="record source identity and hashes for explicitly selected skills")
    adopt.add_argument("--source-url", required=True)
    adopt.add_argument("--branch", default="main")
    adopt.add_argument("--source-root", default="skills", help="directory containing skill directories in the upstream repository")
    adopt.add_argument("--commit", help="full source commit to adopt; must be an ancestor of the fetched branch tip")
    adopt.add_argument("--skills", nargs="+", required=True)
    sub.add_parser("check", help="check canonical and configured projection hashes")
    preview = sub.add_parser("preview", help="show exact upstream diff against a fetched branch tip")
    preview.add_argument("--skill")
    sub.add_parser("update", help="audit and apply eligible upstream changes, then sync and publish")
    approve = sub.add_parser("approve", help="approve one exact fetched commit for removal, rename, or rewritten history")
    approve.add_argument("--skill", required=True)
    approve.add_argument("--commit", required=True)
    approve.add_argument("--reason", required=True)
    exception = sub.add_parser("exception", help="record an exact-hash local exception")
    exception.add_argument("--skill", required=True)
    exception.add_argument("--reason", required=True)
    clear = sub.add_parser("clear-exception", help="clear an exception after restoring adopted source")
    clear.add_argument("--skill", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    root = args.root.resolve()
    try:
        if args.action == "adopt":
            cmd_adopt(root, args)
        elif args.action == "check":
            cmd_check(root)
        elif args.action == "preview":
            cmd_preview(root, args.skill)
        elif args.action == "update":
            cmd_update(root)
        elif args.action == "approve":
            metadata = load_metadata(root)
            if not args.reason.strip():
                raise Blocked("Approval needs a non-empty review reason")
            approve_entry(root, metadata, args.skill, args.commit, args.reason)
        elif args.action == "exception":
            if not args.reason.strip():
                raise Blocked("Exception needs a non-empty reason")
            cmd_exception(root, args)
        elif args.action == "clear-exception":
            cmd_clear_exception(root, args)
        else:
            raise Blocked(f"Unknown action: {args.action}")
    except Blocked as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
