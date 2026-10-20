# Memory and consolidation

Read this reference when durable project knowledge would prevent repeated mistakes, or the user requests memory maintenance or a consolidation ("dreaming") pass.

## Keep the layers distinct

| Layer | Purpose |
|---|---|
| Project instructions | Stable rules and boundaries |
| PLAN.md or existing task tracker | Current objective, sequence, and progress |
| Skills | Reusable procedures |
| Project memory | Durable facts, decisions, and recurring failure patterns |
| Conversation or runner state | Current tool results and unfinished work |

Use the project's existing memory structure. Create only files that serve a concrete need; the guide's folder lists are examples. Keep preferences distinct from technical facts. Store decisions with date, scope, rationale, and evidence. Label inferences and unresolved claims. Store references or sanitized summaries rather than secrets, credentials, or raw private data.

Before updating memory, read its current content, check authority to modify it, and compare the proposed change with current source, tests, logs, or user decisions. Preserve a reviewable diff and rollback path. For concurrent writers, use the storage system's version or content-hash precondition; on conflict, reread and reconcile instead of overwriting another writer. Shared organizational knowledge remains read-only unless write authority is established.

## Consolidation pass

"Dreaming" here means a separate consolidation task, not an assumed Codex product feature. Run it only within the requested scope; scheduling future runs requires an explicit user request and the supported automation tools.

1. Read the selected session notes, current memory, and supporting diffs or validation records.
2. Extract facts likely to matter in future work; discard transient debugging chatter.
3. Verify each candidate and distinguish evidence from inference.
4. Reconcile duplicates, contradictions, and stale statements against current evidence. Retain useful decision history when it explains the current state.
5. Produce exact proposed edits if the user requested proposals; apply edits only when authorized.
6. Report changed knowledge, supporting evidence, and unresolved claims.

Completion means each retained statement has a scope and evidentiary basis, conflicts are resolved or explicit, and the memory diff can be reviewed. A consolidation request does not authorize unrelated code changes or background scheduling.
