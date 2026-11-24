# Office ledger schema

Three JSONL files under `~/.claude/office/`, one record per line. New tasks/handoffs/approvals are appended as a new line. A **status update to an existing task** rewrites that task's existing line in place (read the file, replace the one matching line, write the file back) — there is never more than one line per task `id` in `tasks.jsonl`.

## `tasks.jsonl`

```json
{"id": "<slug>", "chain_id": null, "office": "engineering", "owner_agent": "engineering-head", "title": "<short title>", "status": "queued|active|blocked|needs-approval|done", "linear_id": null, "worktree": null, "created_at": "<ISO8601>", "updated_at": "<ISO8601>"}
```

`chain_id` groups every stage of one multi-office `/office` request (null for a single-stage task, or a single-stage co-pilot-mode task). Each stage still gets its own `id` — `chain_id` is how a reader correlates them, not a replacement for the per-stage id.

`worktree` is the worktree's path when an engineering/quality stage ran isolated — Central Office creates it directly via `git worktree add` (not the native `Agent` tool `isolation` param, which only works relative to Central Office's own session location) — `null` when no worktree was created for that stage. The branch is always named `agent/<chain_id>`, never the head's name. Changes on that branch aren't on the main branch yet; merging it is a `merge`, gated the same as any other, one branch at a time (merging two worktree branches in a batch just moves conflicts to merge time instead of preventing them).

## `handoffs.jsonl`

```json
{"task_id": "<matches tasks.jsonl id>", "from": "central-office", "to": "engineering-head", "at": "<ISO8601>", "summary": "<one line>"}
```

## `approvals.jsonl`

```json
{"task_id": "<id>", "requested_by": "engineering-head", "action": "<one line description>", "status": "pending|approved|rejected", "created_at": "<ISO8601>", "resolved_at": null}
```

## Write ownership

- **Central Office** (the `/office` command) is the only writer of `handoffs.jsonl`, and the only one who creates a task's initial `"queued"` record in `tasks.jsonl`.
- **The owning head** (whichever agent the task's `owner_agent` field names — `engineering-head`, `product-head`, `quality-head`, `research-head`, `design-head`, `data-head`, or `learning-head`) is the only one who updates that record's `status` field afterward, and the only writer of its own `approvals.jsonl` entries.

No office duplicates Linear's or GitHub's state here — a `tasks.jsonl` record stores a real Linear issue ID (for tasks `product-head` filed) plus the office/agent-ownership metadata Linear doesn't have, never the issue content itself.
