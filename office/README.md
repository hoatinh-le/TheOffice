# Two ways to work with this system

**Co-pilot mode** — you call a leaf agent (`pm`, `researcher`, `code-reviewer`, etc.) directly, by name, in your main session. No head agent, no ledger writes, no handoff. You're the orchestrator in real time.

**Office mode** (`/office <request>`) — Central Office classifies the request into a chain of one or more offices, spawns each head in order, tracks it in `tasks.jsonl`/`handoffs.jsonl`, and reports back when the whole chain finishes.

**Which one:** office mode is for anything you're happy to hand off whole, end to end. Anything touching data, money, or auth defaults to co-pilot mode — stay single-threaded and review it closely yourself. This is a rule Central Office enforces on itself, not just a suggestion to you.

## Dashboard

Publish `dashboard.html` as a Claude Code Artifact with the `db` capability (`capabilities: {"db": {}}`), then put the resulting URL here:

Control room: `<YOUR_DASHBOARD_URL>` — approvals and live status get worked here, not in chat. `/office` syncs to it after every stage of every chain (push: local ledgers → dashboard; pull: dashboard approval decisions → local ledgers).
