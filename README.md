# The Office 

A Central Office + specialist-office architecture for [Claude Code](https://claude.com/claude-code): one entry point that classifies a request, routes it to the right specialist, chains multiple specialists automatically when a request needs it, and tracks everything on a live dashboard — while a separate, deliberately lighter "co-pilot mode" stays available for anything you want to drive yourself.

Built across several real build-and-verify sessions, not designed on paper and left untested — every piece here was dispatched for real at least once, with its output independently re-checked rather than taken on the agent's word.

## What's actually in this repo

Only what was originally authored for this system:

- `agents/` — 8 office-head / leaf-worker agent definitions (`engineering-head`, `product-head`, `quality-head`, `research-head`, `design-head`, `data-head`, `data-analyst`, `learning-head`)
- `commands/office.md` — the `/office` entry point: classification, chaining, the mode rule, approval gating, dashboard sync
- `office/SCHEMA.md` — the shared ledger schema (`tasks.jsonl`/`handoffs.jsonl`/`approvals.jsonl`)
- `office/dashboard.html` — the control-room dashboard, a Claude Code Artifact using the `db` runtime capability
- `office/README.md` — the co-pilot-vs-office-mode explainer, installed alongside the ledgers

## What this assumes you already have

This system is a **router and ledger on top of specialist agents** — it is not a complete, self-contained roster. Each office head delegates to leaf agents that aren't included here, because they weren't originally written for this project and aren't mine to redistribute:

- `pm`, `researcher`, `designer`, `qa`, `release-manager`, `frontend-developer`, `code-reviewer` — generic single-purpose agents; write your own versions of these (the head files describe exactly what each is expected to do)
- `codex-rescue` — if you use the official [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc)
- `impeccable-*` design-review agents — from [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0)
- `ecc-architect`, `ecc-tdd-guide`, `ecc-build-error-resolver`, `ecc-security-reviewer` — optional, from the "Everything Claude Code" bundle; `engineering-head`/`quality-head` fall back to the generic agents above if you don't have these

If a referenced agent doesn't exist, the head that calls it will say so rather than silently skip the step — but you'll get more value the more of this roster you actually have.

## Install

1. Copy `agents/*.md` into `~/.claude/agents/`.
2. Copy `commands/office.md` into `~/.claude/commands/`.
3. Copy `office/` into `~/.claude/office/` and create three empty ledger files alongside it:
   ```bash
   touch ~/.claude/office/tasks.jsonl ~/.claude/office/handoffs.jsonl ~/.claude/office/approvals.jsonl
   ```
4. Open `office/SCHEMA.md` and `office/dashboard.html` — publish the dashboard as a Claude Code Artifact (`capabilities: {"db": {}}`), then paste the resulting URL into `office/README.md`.
5. If you want `product-head`'s real Linear write access: connect the official Linear MCP (`claude mcp add --transport http --scope user linear-server https://mcp.linear.app/mcp`), authenticate it, then edit `product-head.md`'s `<YOUR_TEAM_KEY>` placeholder to your real team key (`list_teams` will tell you).
6. Fill in the roster from "What this assumes you already have" above, to whatever depth you want.

## How it works

- **Co-pilot mode**: just talk to Claude Code directly, or name a leaf agent explicitly. No ledger writes, no head layer. Use this for anything you want to stay hands-on for.
- **Office mode** (`/office <request>`): Central Office classifies the request into an ordered chain of offices (a single-stage request if it only names one job, a multi-stage chain if it names several — "spec this and build it" becomes Product → Engineering automatically). Each stage runs, reports back, and syncs to the dashboard before the next one starts. The chain halts — doesn't silently continue — the moment any stage comes back `blocked` or `needs-approval`.
- **The mode rule (hard stop)**: Central Office refuses to spawn `engineering-head` for anything touching data, money, or auth — that work stays in co-pilot mode, reviewed by you directly, no override.
- **The soft gate**: separately, before any Engineering or Quality stage, Central Office checks whether the request targets a platform those workers aren't actually proven for (mobile native, embedded, CLI-only, desktop-native — they're documented for web). If so, it stops and asks you to confirm office mode rather than silently assuming it'll go well. Unlike the hard stop, you can say "proceed anyway."
- **`product-head`'s own three-step process**: validate (logical pressure-test via `pm` *and* a real market-signal check via `researcher` applying `last30days`-style recency discipline) → plan the bare-bones MVP (via `ecc-planner` or `planning-and-task-breakdown`) → spec exactly that scope. An idea that fails validation gets reported as a dead end, not forced into a spec nobody asked for.
- **The evidence gate**: every head is written to reject "this works" as proof. It requires the actual observed test output, a real benchmark, or a real evidence trail (a commit, a metric, a quoted doc line) — never a worker's narration alone.
- **The approval gate**: git push/merge/deploy, destructive operations, purchases, and financial transactions are never performed by any head. They get queued (`approvals.jsonl` + the dashboard) and wait for you — silence means still pending, never approved. Linear issue *creation* is the one explicit exception, carved out as autonomous draft-level work; updating or deleting an existing issue is not.

## A known platform quirk

Editing an agent, command, or newly-connected MCP server doesn't always take effect on the very next dispatch in an already-running session — tool/agent registries and MCP connections get built once and don't always refresh live. Every time this was hit during development, the affected agent or command caught it itself (a "tool not found" error, or the agent noticing its own instructions didn't match what it was asked to do) rather than silently misbehaving — that self-check is itself part of the design, not a lucky accident. A fresh session is the reliable fix if you hit it.

## Inspiration

The idea of a Central Office routing to specialist offices was adapted from the general shape of multi-agent "AI team" setups circulating for Claude Code (including [bekhruztbx/ai-creative-team](https://github.com/bekhruztbx/ai-creative-team)) — adapted here for research, product, design, engineering, QA, data, and learning work rather than content creation, with a persistent ledger, real approval gating, and a live dashboard added on top.

## License

MIT for the files in this repo. See "What this assumes you already have" for the licenses of agents this system depends on but doesn't include.
