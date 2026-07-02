# Test-Agent Memory Log

Running log of Test-Agent's reviews, test cases written, and reasoning.
Same convention as the root [`memory.md`](../memory.md), scoped to this
agent's work.

Convention (read before adding an entry):
- Newest entry at the top (reverse-chronological).
- One entry per *meaningful* event: a test-coverage review performed
  (pass or fail), a coverage gap raised, a constraint or check added to
  `CLAUDE.md` / `SKILLS.md`, or a blocking finding escalated to the user.
- Not for routine/no-decision edits (typo fixes, formatting-only diffs).
- Entries are append-only — do not edit past entries except to fix
  factual errors, and mark the fix inline rather than silently rewriting
  history.
- Entry header format: `## YYYY-MM-DD — <short title>`

Entry template:

```
## YYYY-MM-DD — <short title>

**What changed (function/module under test):**
- ...

**Test cases added/updated:**
- ...

**Result (pass/fail, coverage gaps):**
- ...

**Open questions / what's next:**
- ...
```

---

## 2026-07-01 — Test-Agent created

> **Correction (same day):** The "Why" below originally said Test-Agent
> was "a new Member Agent under the Engineering plugin." That's wrong —
> Test-Agent is an engineering co-worker agent that helps build this
> project, not an entity inside the org's own multi-agent architecture
> (see root `memory.md`, 2026-07-01 correction entry). Left as-is per the
> append-only convention; corrected charter now lives in `CLAUDE.md`.

**What changed (function/module under test):**
- N/A — this is the agent's creation entry, not a test review.

**Test cases added/updated:**
- N/A.

**Result (pass/fail, coverage gaps):**
- N/A.

**Why:**
- Test-Agent added as a new Member Agent under the Engineering plugin
  (`swarm-trading-system-plan.md` §9.2), alongside Security-Agent.
  Charter: write test cases for CI/CD whenever a new function or change
  needs verification before merge to `master`. See this folder's
  `CLAUDE.md` and `SKILLS.md` for the full charter and operational
  checklist.

**Open questions / what's next:**
- No CI pipeline exists yet — this folder currently documents the
  agent's intended role only (repo is still planning-only per root
  `CLAUDE.md`).
- First real test review will happen once there are actual
  functions/modules to cover.

---

## 2026-07-01 — Constraints added: auth test suite, paper-trading-only tests

**What changed (function/module under test):**
- N/A — charter update, not a test review (no code exists yet).

**Test cases added/updated:**
- N/A.

**Result (pass/fail, coverage gaps):**
- N/A.

**Why:**
- Follow-up to Security-Agent's new JWT/session-auth constraint
  (`Security-Agent/CLAUDE.md`): added a matching non-negotiable
  constraint requiring an explicit auth test suite (expired/tampered JWT
  rejected, revoked session loses access, direct-URL route access denied
  without a valid session) for any auth-touching change, so the
  constraint is test-enforced, not just review-enforced.
- Also added a paper-trading-only rule for any test touching real order
  placement/broker connectors/trade execution, making root `CLAUDE.md`'s
  "no live trading until backtesting + paper trading both show
  acceptable behavior" constraint concrete at the test-authoring level.
  User approved both. Added to `CLAUDE.md` (two new "Non-negotiable
  constraints" bullets) and `SKILLS.md` §3 (two new bullets in
  "Coordination on cross-cutting concerns").

**Open questions / what's next:**
- No auth code or trading/broker code exists yet to write these tests
  against — applies once that code exists.
