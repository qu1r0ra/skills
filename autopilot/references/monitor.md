# Autopilot monitor

Read the supplied `monitor-brief.md`. Resolve its absolute report path and
orchestrator thread ID. If pending, obtain the ID from the newly started
orchestrator session and fill the brief before monitoring; never guess a
thread. Use the other provider selected in the approved kickoff.

Create one hourly observation task bound to this session. Retain its ID in
the monitor brief and report its cadence and next run time. This watcher is
distinct from any draft-only activation deliverable in the plan. On resume,
inspect the recorded task before creating another. If scheduling or thread
access is unavailable, report the exact limitation; claim monitoring active
only after the task exists and the thread is readable. Completion: the brief
identifies the verified watcher and thread, or the missing capability.

## Observation and wake decisions

At each check, read the live thread status and living report. Reconcile the
last wake, observed evidence, retry due times and schedule state in the monitor
brief. Use the frontier's release conditions, not report wording alone:

1. If either source cannot be read, record incomplete evidence. Notify the
   owner on first occurrence or a material change; retain the next observation
   while recovery is possible. Completion: the unavailable source and retry
   are recorded, with no invented progress claim.
2. If `Run status: done`, send the owner the top handover items and report link
   once. Delete this monitor's task by its recorded ID and verify deletion.
   Record failed deletion and retry it on the next check without repeating
   handover. Completion: handover was sent and the watcher is verified absent.
3. Otherwise classify what can advance. An idle orchestrator merits one resume
   message when approved work is dispatchable, a child/check result is newly
   available, a recoverable retry is due, or new evidence satisfies a recorded
   release condition. A due provider retry warrants a wake even if the report
   text is unchanged. Include the reason, evidence or due time, report path
   and instruction to reconcile live state before continuing. Record the wake
   and retry it only after its bounded recovery window or a new event; allow
   at most one resume message per check. An active orchestrator needs no
   duplicate resume. Completion: each eligible wake is sent or its active-task
   suppression is recorded.
4. For unchanged owner gates or unavailable capabilities with no due recovery,
   record the evidence or decision needed; send no identical hourly resume or
   owner notification. Notify the owner of material progress, a new decision
   or a changed failure. When only these stable gates remain and there are no
   active children, pending checks or due/future retries, send the held handover
   once, then delete this watcher and verify absence. Record the parked state
   and how monitoring can be restarted after the release condition changes.
   A held handover does not mark the run done. If recoverable work remains,
   retain hourly observation. Completion: the next observation or parked
   release condition is explicit and the schedule disposition is verified.

An unrecorded retry condition requires reconciliation, not an endless series
of identical resumes. Ask the orchestrator once to establish a bounded retry
or named release condition, then surface unresolved evidence as a monitoring
hold. The monitor observes and wakes; implementation, dispatch, owner decisions
and run completion remain with the orchestrator. It expands no approval and
creates no recovery timer for the orchestrator.
