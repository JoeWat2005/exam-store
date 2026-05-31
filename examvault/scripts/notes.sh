#!/bin/bash

NOTES_TXT="/jupyter/work/exam-store/notes.txt"
NOTES_MD="/jupyter/work/exam-store/examvault/NOTES.md"
MODEL="/jupyter/work/exam-store/examvault/models/gen.llamafile"

# Exit silently if input or model is missing
[ -f "$NOTES_TXT" ] || exit 1
[ -x "$MODEL" ] || exit 1

# Start notes file
echo "# Haskell Notes" > "$NOTES_MD"
echo >> "$NOTES_MD"

# Function to clean model output
clean_code() {
    sed '/<|im_end|>/q' |
    sed '/^```/d' |
    sed 's/```haskell//g' |
    grep -v '<|im_' |
    grep -v '^system$' |
    grep -v '^user$' |
    grep -v '^assistant$' |
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
    grep -v '^$' |
    head -20
}

# Read notes line by line
while IFS= read -r line || [ -n "$line" ]; do
    [ -z "$line" ] && continue
    [[ "$line" =~ ^# ]] && continue

    signature="${line%% - *}"
    context="${line#* - }"

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
            --silent-prompt \
            --chat-template chatml \
            --log-disable \
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
