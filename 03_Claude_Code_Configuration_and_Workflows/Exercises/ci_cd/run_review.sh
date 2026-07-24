#!/usr/bin/env bash
# Example CI/CD review step — run Claude Code non-interactively over a PR diff
# and emit machine-parseable, schema-validated findings for inline PR comments.
#
# Maps to Task 3.6 (Integrate Claude Code into CI/CD pipelines) and
# Theory/03_Iterative_Refinement_and_CICD.md.
#
# This script is meant to be read, not executed against a real API key blindly —
# see README.md in this folder for how to try it safely.
set -euo pipefail
cd "$(dirname "$0")"

BASE_BRANCH="${1:-main}"
PRIOR_FINDINGS_FILE="prior_findings.json"   # produced by a previous run of this script, if any
OUTPUT_FILE="review_findings.json"

echo "=== Claude Code CI Review: diff against ${BASE_BRANCH} ===" >&2

# Build the prompt. If a prior review already ran on this PR, we include its
# findings so Claude reports only NEW or still-unaddressed issues instead of
# re-flagging everything on every commit (see Theory/03 — "avoiding duplicate
# findings across re-runs").
PROMPT="Review the diff between HEAD and ${BASE_BRANCH} for correctness bugs, \
security issues, missing test coverage, and documentation gaps. \
Follow the review criteria and fixture conventions documented in this \
repository's CLAUDE.md and .claude/rules/ files — do not invent your own \
criteria. Only flag concrete, actionable issues; do not pad the findings \
list with generic style comments to seem thorough."

if [ -f "${PRIOR_FINDINGS_FILE}" ]; then
  PROMPT="${PROMPT} A prior review already ran on this PR; its findings are \
attached below. Mark any finding that duplicates one already reported and \
still unaddressed with is_new=false — do not repeat it as a new comment. \
Prior findings: $(cat "${PRIOR_FINDINGS_FILE}")"
fi

# -p / --print: required for CI — without it, Claude Code waits for interactive
# input and the pipeline job hangs instead of completing or failing cleanly.
#
# --output-format json + --json-schema: forces machine-parseable output that
# matches schema.json exactly, so downstream steps can post one inline PR
# comment per finding instead of dumping an unstructured wall of text.
claude -p "${PROMPT}" \
  --output-format json \
  --json-schema schema.json \
  > "${OUTPUT_FILE}"

echo "=== Wrote ${OUTPUT_FILE} ===" >&2

# Downstream step (not shown): read $OUTPUT_FILE, filter to findings where
# is_new == true, post one PR review comment per finding at file:line, and
# save $OUTPUT_FILE as $PRIOR_FINDINGS_FILE for the next run on this PR.
cp "${OUTPUT_FILE}" "${PRIOR_FINDINGS_FILE}"

# Fail the pipeline if any blocking finding is new and unaddressed.
BLOCKING_COUNT=$(python3 -c "
import json
data = json.load(open('${OUTPUT_FILE}'))
blocking = [f for f in data['findings'] if f['severity'] == 'blocking' and f.get('is_new', True)]
print(len(blocking))
")

if [ "${BLOCKING_COUNT}" -gt 0 ]; then
  echo "=== ${BLOCKING_COUNT} new blocking finding(s) — failing pipeline ===" >&2
  exit 1
fi

echo "=== No new blocking findings ===" >&2
