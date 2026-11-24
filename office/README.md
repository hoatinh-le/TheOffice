# Two ways to work with this system

**Co-pilot mode** — you call `pm`, `researcher`, `code-reviewer`, or `frontend-developer` directly, by name, in your main session. No head agent, no ledger writes, no handoff. You're the orchestrator in real time.

**Office mode** (`/office <request>`) — Central Office classifies the request, spawns the relevant head, tracks it in `tasks.jsonl`/`handoffs.jsonl`, and reports back at the end.

**Which one:** office mode is for research, low-stakes work, and anything well-specified enough to hand off whole — it can now chain multiple offices automatically (e.g. "spec this and build it" runs Product then Engineering in one `/office` call). Anything touching data, money, or auth defaults to co-pilot mode — stay single-threaded and review it closely yourself, hard stop, no override. Separately, `/office` also runs a *soft* check before any Engineering or Quality stage: if the request is for a non-web platform (mobile native, embedded, CLI, desktop-native), it'll flag that those workers are only proven for web and ask you to confirm before proceeding in office mode rather than silently assuming it'll go well.

All 7 offices exist: Engineering, Product, Quality, Research, Design, Data & Portfolio, Learning.

## Starting a new idea — the pattern, not an office

Before any office gets involved, idea validation itself stays co-pilot: run `pm` (logical pressure-test — who it's for, the real assumption, the smallest version, the failure mode) *and* a `last30days`-style check via `researcher` (is there real recent signal anyone wants this) side by side. A logically sound idea with zero market signal is still a thin case.

If it survives both but still has open design questions, run the `grilling` skill (or `grill-with-docs` if you want it writing `GLOSSARY.md`/ADRs as it goes) before handing off — it interviews *you* directly with yes/no questions until the design tree resolves. This only works here, in co-pilot mode, because it needs you answering live; a spawned head agent inside a `/office` chain has no one to interview.

Once it survives validation (and grilling, if used), `/office "spec this and build it"` picks up from there — `product-head` runs its own validate → plan-the-MVP → spec sequence before any code gets written.

## Approvals

No dashboard — approvals and status are worked directly in chat. When a stage hits a gated action (git push/merge, an external MCP write, a purchase, anything destructive), `/office` stops the chain, tells you exactly what's pending, and waits for your word. Say "approved" or "rejected" and it resolves the ledger and, if approved, performs the action and resumes the chain.

## Running multiple agents at once

Engineering/Quality stages isolate via a real `git worktree add` that Central Office runs itself (`git -C <repo> worktree add ../<repo>-<chain_id> -b agent/<chain_id>`) — not Claude Code's native `Agent`-tool `isolation` param, which only isolates relative to wherever the calling session already is and fails outside a git repo. Because Central Office runs the `git worktree add` directly, this works for any repo path, regardless of where you launched `claude` from.

Each worktree gets `.env*` files copied in and the project's install command run (`npm ci`/etc., detected from the lockfile) — a fresh worktree has neither by default, and is unusable without them.

**Still yours to handle, not something `/office` can solve generically:** dev-server port collisions and any shared database/Redis instance across worktrees of the same repo — derive a port from the worktree/chain id in your own project if you'll run more than one server at once, and don't point two worktrees' tests at the same live database.

**Merging:** one worktree branch at a time — `git diff main..agent/<chain_id>` before merging, rebase the worktree onto main after each merge. Worktrees isolate working copies, not what the branches merge into, so batching merges just moves conflicts to merge time instead of preventing them.

What's still not covered: the shared ledger (`tasks.jsonl`/`handoffs.jsonl`/`approvals.jsonl`) lives outside git and has no locking. Two sessions both running `/office` at the same moment can still race on it — worst case is a rare duplicate task record, not lost code. Real locking would need the office heads to have `Bash` (they deliberately don't) or a rework of the ledger into an append-only event log — a real build, not done yet.
