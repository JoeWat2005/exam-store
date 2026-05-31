#!/bin/bash

# =============================================================================
# NOTEGENERATOR
# =============================================================================
# What this is:
#   A batch note generator. It reads a plain-text list of Haskell exercises and
#   produces a single Markdown study file, one section per exercise. It is meant
#   to be run headless (no arguments, no prompts) — e.g. a one-line shell call.
#
# Input:
#   notes.txt — lives in the UPPER directory: the folder that contains this
#   examvault directory alongside `other/` and `revision/`. Each non-empty,
#   non-comment line is one entry in the form:
#       <type signature> - <description of what to implement>
#   (Blank lines and lines starting with '#' are skipped.)
#
# Output:
#   NOTES.md — written into the INNER examvault directory, right next to
#   NAVIGATION.md, HOME.md, KNOWLEDGE-MAP.md, etc. Any existing NOTES.md is
#   overwritten from scratch on every run.
#
# How it works:
#   1. All paths are resolved relative to this script's OWN location, so it is
#      portable: copy the tree anywhere and run it from any working directory
#      and it still finds notes.txt, the generator, and the output folder.
#   2. NOTES.md is started with a top-level "# Haskell Notes" heading.
#   3. For every entry in notes.txt:
#        - split the line into the signature (text before " - ") and the
#          description (text after " - ");
#        - build a ChatML prompt that asks for Haskell source only;
#        - feed that prompt to the bundled generator, models/gen.llamafile,
#          in single-shot --cli mode with deterministic settings (--temp 0);
#        - pass the raw output through clean_code() to strip prompt echoes,
#          markdown fences and stray prose, keeping just the code (max 20 lines);
#        - append a "## <signature>" section containing the cleaned code inside
#          a ```haskell fenced block.
#   4. Print "Done." once the whole list has been processed.
#
# Notes:
#   - models/gen.llamafile is invoked with --log-disable so it does NOT drop a
#     main.log trace file beside the script on each run.
#   - This script and models/gen.llamafile must be executable (chmod +x) to run.
# =============================================================================

# --- Resolve paths relative to this script (portable / headless-safe) --------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # .../examvault/scripts
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"                    # inner examvault (NAVIGATION.md lives here)
ROOT_DIR="$(cd "$VAULT_DIR/.." && pwd)"                      # upper dir (notes.txt lives here)

NOTES_TXT="$ROOT_DIR/notes.txt"
NOTES_MD="$VAULT_DIR/NOTES.md"
MODEL="$VAULT_DIR/models/gen.llamafile"

echo "# Haskell Notes" > "$NOTES_MD"
echo >> "$NOTES_MD"

clean_code() {
    sed '/<|im_end|>/q' |
    sed '/^```/d' |
    sed 's/```haskell//g' |
    grep -v '<|im_' |
    grep -v '^Certainly' |
    grep -v '^Here' |
    grep -v '^Explanation' |
    grep -v '^Example' |
    grep -v '^You are' |
    grep -v '^Implement' |
    grep -v '^Requirements:' |
    grep -v '^Output' |
    grep -v '^Task:' |
    grep -v '^Rules:' |
    head -20
}

while IFS= read -r line; do
    [ -z "$line" ] && continue
    [[ "$line" =~ ^# ]] && continue

    signature="$(printf '%s\n' "$line" | sed 's/ - .*//')"
    context="$(printf '%s\n' "$line" | sed 's/^[^-]* - //')"

    PROMPT="<|im_start|>system
You are a Haskell programming assistant. Output only Haskell code. No explanations. No markdown.
<|im_end|>
<|im_start|>user
Implement:

$signature

Requirements:
$context
<|im_end|>
<|im_start|>assistant
"
    PASS=$(
        "$MODEL" \
            --cli \
            --log-disable \
            --silent-prompt \
            --chat-template chatml \
            -n 96 \
            --temp 0 \
            -p "$PROMPT" \
            2>/dev/null
    )

    FINAL_CODE="$(echo "$PASS" | clean_code)"

    {
        echo "## $signature"
        echo
        echo '```haskell'
        echo "$FINAL_CODE"
        echo '```'
        echo
    } >> "$NOTES_MD"

done < "$NOTES_TXT"

echo "Done."
