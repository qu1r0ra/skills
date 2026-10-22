# Autopilot monitor

Read the supplied `monitor-brief.md`. Resolve its absolute report path and
orchestrator thread ID. If the ID is pending, obtain it from the newly started
orchestrator session and fill the brief before monitoring; never guess a thread.
Use the other provider selected in the approved kickoff.

Create one hourly monitor task bound to this session, retain its scheduled-task
ID in the monitor brief, and report its cadence and next run time. This task
is the run's watcher, distinct from any draft-only activation deliverable in
the work plan. On resume, inspect the recorded task before creating another.
If scheduling or thread access is unavailable, report the exact limitation;
claim monitoring active only after its task exists and the thread is readable.

At each hourly check:

1. Read the orchestrator thread's current status and the living report. If
   either cannot be read, report the missing evidence to the owner and retain
   the monitor task for the next check.
2. If the report says `Run status: done`, send the owner the top items from its
   handover guide, with the report link. Then delete this monitor's own
   scheduled task using its recorded ID and verify deletion. Report a failed
   deletion explicitly and retry cleanup on the next check. Monitoring ends
   only when the handover was sent and that task is deleted.
3. Otherwise, if the thread is idle while its frontier is non-empty, or the
   report carries `held, needs wake`, send the orchestrator one resume message
   for this check. Name the report and ask it to reconcile in-flight task
   status and continue the approved plan. When both conditions apply, send
   only one message.
4. Otherwise report the current state to the owner from the report, including
   the frontier or owner gates. Keep the next hourly check active.

The monitor observes and wakes the orchestrator; implementation, dispatch and
run completion remain with the orchestrator. It does not expand the plan.
