# SKILLS.md — Test-Agent

Operational detail behind the charter in [`CLAUDE.md`](CLAUDE.md): what
Test-Agent actually does when new work needs coverage before merging to
`master`. Planning-only for now — no CI pipeline exists yet, so this is
the spec a future implementation (or a manual review pass) should follow.

## 1. When Test-Agent engages

- Any new function, module, or public interface added.
- Any change to existing behavior (bug fix, refactor, dependency bump)
  that could alter observable output.
- Any pull request targeting `master`, as the last gate before merge —
  this is the CI/CD trigger point per this agent's charter.

## 2. What a test case must cover

For each function/behavior under test:
- **Golden path** — the documented/intended use case, with realistic
  inputs.
- **Edge cases** — empty/null input, boundary values (zero, negative,
  max size), unexpected types, concurrent/duplicate calls if relevant.
- **Failure modes** — what should happen when a dependency is
  unavailable, a network/connector call fails, or input is malformed;
  confirm failures are handled explicitly, not silently swallowed
  (consistent with this project's "nothing executes silently" audit
  principle from root `CLAUDE.md`).
- **Regression coverage** — for bug fixes, a test that reproduces the
  original bug and would fail without the fix.

## 3. Coordination on cross-cutting concerns

- **Trading hard-rules / kill switch code** (if/when it exists): any
  change touching that gate or the manual override needs a test proving
  it cannot be bypassed — not just that it works on the happy path.
  Treat this class of test as blocking, not optional.
- **Security-Agent overlap**: when Security-Agent flags a finding (e.g.,
  missing input validation), Test-Agent writes the regression test that
  proves the fix — a test reproducing the exploit path failing safely.
  Security-Agent and Test-Agent should not duplicate each other's
  review, but a security fix without a corresponding test is incomplete.
- **Auth test suite** (JWT / session, per Security-Agent's charter):
  every auth-touching change needs tests for — expired/tampered JWT
  rejected; revoked/logged-out session cannot still access protected
  routes; a protected route/endpoint requested directly by URL/path
  (no UI navigation) is denied without a valid, authorized session. This
  is the concrete regression coverage for Security-Agent's "no route
  reachable without authorization" constraint.
- **Connector integrations** (Robinhood, Github, Excalidraw, Goodnotes,
  AgentMail): prefer mocked/stubbed connector responses in tests over
  live calls, so CI doesn't depend on external service availability or
  risk real side effects (e.g., a live trade).
- **Paper-trading-only for live-money-adjacent tests**: any test that
  exercises real order placement, broker connector calls, or trade
  execution must target a paper-trading/sandbox account. Never point a
  test — automated or a "quick manual check" — at a live account, per
  root `CLAUDE.md`'s no-live-trading-before-paper-trading constraint.

## 4. How results are reported

- Each CI/CD-facing review produces: what changed, what test cases were
  added or updated, pass/fail result, and any coverage gaps found but not
  yet closed.
- A missing-coverage or failing-test finding blocks merge — raise it to
  the user directly, don't wave it through.
- Every review — pass or fail — gets an entry in this folder's
  `memory.md`, per the append-only convention in `CLAUDE.md`, so the
  reasoning behind a merge decision isn't lost.
