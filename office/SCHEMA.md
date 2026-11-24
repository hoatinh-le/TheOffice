# Office ledger schema

Three JSONL files under `~/.claude/office/`, one record per line. New tasks/handoffs/approvals are appended as a new line. A **status update to an existing task** rewrites that task's existing line in place (read the file, replace the one matching line, write the file back) — there is never more than one line per task `id` in `tasks.jsonl`.

## `tasks.jsonl`

```json
{"id": "<slug>", "chain_id": null, "office": "engineering", "owner_agent": "engineering-head", "title": "<short title>", "status": "queued|active|blocked|needs-approval|done", "linear_id": null, "created_at": "<ISO8601>", "updated_at": "<ISO8601>"}
```

`chain_id` groups every stage of one multi-office `/office` request (null for a single-stage task, or a single-stage co-pilot-mode task). Each stage still gets its own `id` — `chain_id` is how the dashboard and a reader correlate them, not a replacement for the per-stage id.

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

No office duplicates Linear's or GitHub's state here — a `tasks.jsonl` record stores a Linear issue ID (once Linear is connected) plus the office/agent-ownership metadata Linear doesn't have, never the issue content itself.
