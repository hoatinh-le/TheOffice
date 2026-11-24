# Two ways to work with this system

**Co-pilot mode** — you call a leaf agent (`pm`, `researcher`, `code-reviewer`, etc.) directly, by name, in your main session. No head agent, no ledger writes, no handoff. You're the orchestrator in real time.

**Office mode** (`/office <request>`) — Central Office classifies the request into a chain of one or more offices, spawns each head in order, tracks it in `tasks.jsonl`/`handoffs.jsonl`, and reports back when the whole chain finishes.

**Which one:** office mode is for anything you're happy to hand off whole, end to end — it chains multiple offices automatically when a request names several stages. Anything touching data, money, or auth defaults to co-pilot mode, hard stop, no override. Separately, a *soft* gate asks you to confirm before any Engineering/Quality stage targeting a platform those workers aren't actually proven for (mobile native, embedded, CLI, desktop — they're documented for web).

## Dashboard

Publish `dashboard.html` as a Claude Code Artifact with the `db` capability (`capabilities: {"db": {}}`), then put the resulting URL here:

Control room: `<YOUR_DASHBOARD_URL>` — approvals and live status get worked here, not in chat. `/office` syncs to it after every stage of every chain (push: local ledgers → dashboard; pull: dashboard approval decisions → local ledgers).

## Running multiple agents at once

Engineering/Quality stages isolate via a real `git worktree add` that Central Office runs itself (`git -C <repo> worktree add ../<repo>-<chain_id> -b agent/<chain_id>`), not Claude Code's native `Agent`-tool `isolation` param (that only isolates relative to wherever the calling session already is, and fails outside a git repo). Because Central Office runs `git worktree add` directly, this works for any repo path regardless of where you launched `claude` from.

Each worktree gets `.env*` files copied in and the project's install command run (detected from the lockfile) — a fresh worktree has neither by default.

**Still yours to handle:** dev-server port collisions and any shared database across worktrees of the same repo — not something `/office` can solve generically.

**Merging:** one worktree branch at a time — diff before merging, rebase onto main after each merge. Worktrees isolate working copies, not what branches merge into.

What's still not covered: the shared ledger lives outside git with no locking — two sessions running `/office` at once can still race on it. Worst case is a rare duplicate task or a dashboard glitch, not lost code. Real locking would need the office heads to have `Bash` (they deliberately don't) or an append-only ledger redesign — not built yet.
