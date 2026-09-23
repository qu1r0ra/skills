# Protect designated upstream skills

Only skills explicitly listed in `.metadata.json` receive upstream maintenance; the manifest records each source identity, adopted revision, complete directory hash, and file hashes. The updater blocks canonical drift and source removals or renames, audits accepted upstream changes, updates only designated directories, and checks their SkillShare projections. Local behavior belongs in separate wrappers or forks so upstream refreshes can restore the source faithfully.
