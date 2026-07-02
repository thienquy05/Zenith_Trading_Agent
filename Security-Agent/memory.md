# Security-Agent Memory Log

Running log of Security-Agent's reviews, findings, and reasoning. Same
convention as the root [`memory.md`](../memory.md), scoped to this
agent's work.

Convention (read before adding an entry):
- Newest entry at the top (reverse-chronological).
- One entry per *meaningful* event: a security review performed (pass or
  fail), a finding raised, a constraint or check added to `CLAUDE.md` /
  `SKILLS.md`, or a blocking finding escalated to the user.
- Not for routine/no-decision edits (typo fixes, formatting-only diffs).
- Entries are append-only — do not edit past entries except to fix
  factual errors, and mark the fix inline rather than silently rewriting
  history.
- Entry header format: `## YYYY-MM-DD — <short title>`

Entry template:

```
## YYYY-MM-DD — <short title>

**What was reviewed:**
- ...

**Findings:**
- ...

**Why (severity / reasoning):**
- ...

**Open questions / what's next:**
- ...
```

---

## 2026-07-01 — Security-Agent created

> **Correction (same day):** The "Why" below originally said Security-Agent
> was "a new Member Agent under the Engineering plugin." That's wrong —
> Security-Agent is an engineering co-worker agent that helps build this
> project, not an entity inside the org's own multi-agent architecture
> (see root `memory.md`, 2026-07-01 correction entry). Left as-is per the
> append-only convention; corrected charter now lives in `CLAUDE.md`.

**What was reviewed:**
- N/A — this is the agent's creation entry, not a code review.

**Findings:**
- N/A.

**Why (severity / reasoning):**
- Security-Agent added as a new Member Agent under the Engineering
  plugin (`swarm-trading-system-plan.md` §9.2), alongside Test-Agent.
  Charter: review code for exploitable flaws, and specifically enforce
  that credentials/sensitive data are always encrypted at rest with
  strong database-level validation and access restriction. See this
  folder's `CLAUDE.md` and `SKILLS.md` for the full charter and
  operational checklist.

**Open questions / what's next:**
- No scanning tooling or CI hook exists yet — this folder currently
  documents the agent's intended role only (repo is still planning-only
  per root `CLAUDE.md`).
- First real review will happen once there's actual code to review.

---

## 2026-07-01 — Constraint added: JWT/session auth, no route backdoors

**What was reviewed:**
- N/A — this is a charter update, not a code review (no auth code exists
  yet).

**Findings:**
- N/A.

**Why (severity / reasoning):**
- User specified the platform will authorize users via JWT plus a
  server-side session token, and that protected routes/pages (example
  given: `ai_trading/dashboard`) must never be reachable just by
  requesting the URL directly — no backdoor access via unlinked or
  hidden routes. Added as a non-negotiable constraint in `CLAUDE.md`
  (new bullet under "Non-negotiable constraints") and as a new
  operational section in `SKILLS.md` (§3, "Authentication &
  authorization (JWT / session tokens)"), covering JWT signature/expiry
  validation, revocable session tokens, server-side default-deny
  authorization per route, and treating any debug/override bypass as a
  critical finding regardless of environment.

**Open questions / what's next:**
- No auth implementation exists yet to review against this constraint —
  applies once the platform's login/session/routing code is written.

---

## 2026-07-01 — Constraints added: rate limiting, CSRF, tamper-evident audit log

**What was reviewed:**
- N/A — charter update following up on the JWT/session constraint above,
  not a code review (no code exists yet).

**Findings:**
- N/A.

**Why (severity / reasoning):**
- Follow-up recommendation after adding the JWT/session-auth constraint:
  closing the two classic follow-on gaps (brute-forceable auth endpoints,
  CSRF on cookie-based sessions) and tying the existing audit-log
  requirement (root `CLAUDE.md`) to tamper-evidence, not just presence.
  User approved adding all three. Added to `CLAUDE.md` (three new
  "Non-negotiable constraints" bullets) and `SKILLS.md` (rate
  limiting/CSRF folded into §3 auth section; new §4 "Audit log
  integrity"; sections renumbered accordingly, §4–5 -> §5–6, old §6 ->
  §7).
- CSRF is conditioned on session tokens actually living in cookies —
  not applicable to pure header-based bearer tokens. Left as a
  check-before-flagging note in `SKILLS.md` rather than an unconditional
  rule, since the platform's actual token transport isn't decided yet.

**Open questions / what's next:**
- Confirm, once auth is designed, whether session tokens use cookies or
  headers — determines whether the CSRF constraint is live or moot.
- No implementation exists yet to review against any of these three
  constraints.
