# Two ways to work with this system

**Co-pilot mode** — you call a leaf agent (`pm`, `researcher`, `code-reviewer`, etc.) directly, by name, in your main session. No head agent, no ledger writes, no handoff. You're the orchestrator in real time.

**Office mode** (`/office <request>`) — Central Office classifies the request into a chain of one or more offices, spawns each head in order, tracks it in `tasks.jsonl`/`handoffs.jsonl`, and reports back when the whole chain finishes.

**Which one:** office mode is for anything you're happy to hand off whole, end to end — it chains multiple offices automatically when a request names several stages. Anything touching data, money, or auth defaults to co-pilot mode, hard stop, no override. Separately, a *soft* gate asks you to confirm before any Engineering/Quality stage targeting a platform those workers aren't actually proven for (mobile native, embedded, CLI, desktop — they're documented for web).

## Dashboard

Publish `dashboard.html` as a Claude Code Artifact with the `db` capability (`capabilities: {"db": {}}`), then put the resulting URL here:

Control room: `<YOUR_DASHBOARD_URL>` — approvals and live status get worked here, not in chat. `/office` syncs to it after every stage of every chain (push: local ledgers → dashboard; pull: dashboard approval decisions → local ledgers).

## Running multiple agents at once

Worktree isolation (`isolation: "worktree"` on the `Agent` call) is how Engineering/Quality stages avoid colliding on the same repo when more than one runs concurrently. **This only works when the Claude Code session itself is launched from inside the target project's git repo** — `cd` into your project before running `claude`, not from your home directory.

What it doesn't cover: the shared ledger lives outside git with no locking — two sessions running `/office` at once can still race on it. Worst case is a rare duplicate task or a dashboard glitch, not lost code. Real locking would need the office heads to have `Bash` (they deliberately don't) or an append-only ledger redesign — not built yet.
