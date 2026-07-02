#!/bin/bash
# SessionStart hook: keep the codebase-memory-mcp knowledge graph fresh.
#
# Detects whether the git tree changed since the last index (tracked
# content via `git diff HEAD`, plus the set of untracked files) and only
# re-indexes when it actually differs -- i.e. "detect changes if need".
# When nothing changed this is a couple of cheap git calls and exits 0.
#
# Never blocks a session: any failure is silent (exit 0, no output).

set -u

# Resolve the indexer binary (PATH first, then the known install location).
BIN="$(command -v codebase-memory-mcp 2>/dev/null || true)"
[ -n "$BIN" ] || BIN="C:/Users/thien/AppData/Local/Programs/codebase-memory-mcp/codebase-memory-mcp.exe"
[ -x "$BIN" ] || command -v "$BIN" >/dev/null 2>&1 || exit 0

# Repo root as a forward-slash path (valid for both `cd` and the JSON payload).
REPO="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "$REPO" ] || exit 0
cd "$REPO" 2>/dev/null || exit 0

SIG_DIR="$REPO/.codebase-memory"
SIG_FILE="$SIG_DIR/.autoindex-sig"

# Signature changes whenever committed HEAD, uncommitted tracked content,
# or the set of untracked files changes.
head="$(git rev-parse HEAD 2>/dev/null || echo none)"
diff="$(git diff HEAD 2>/dev/null || true)"
untracked="$(git ls-files --others --exclude-standard 2>/dev/null || true)"
sig="$(printf '%s\n%s\n%s' "$head" "$diff" "$untracked" | sha256sum | cut -d' ' -f1)"

prev="$(cat "$SIG_FILE" 2>/dev/null || true)"
if [ "$sig" = "$prev" ]; then
  exit 0   # graph already reflects the current tree
fi

# Tree changed -> re-index (fast mode: filtered files, no similarity edges).
# Only record the new signature if the re-index actually succeeded, so a
# failed run is retried next session instead of being marked fresh.
if "$BIN" cli index_repository "{\"repo_path\":\"$REPO\",\"mode\":\"fast\"}" >/dev/null 2>&1; then
  mkdir -p "$SIG_DIR" 2>/dev/null || true
  printf '%s' "$sig" > "$SIG_FILE" 2>/dev/null || true
  echo '{"systemMessage":"codebase-memory: git tree changed since last index -- re-indexed the graph (fast mode)."}'
fi

exit 0
