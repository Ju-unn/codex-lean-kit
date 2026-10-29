#!/bin/sh
# Copy the kit's skills, agent roles, and AGENTS.md into the current workspace without overwriting anything.
# Usage (from the workspace root): sh /path/to/codex-lean-kit/install.sh
set -eu

KIT=$(cd "$(dirname "$0")" && pwd)
DEST=$(pwd)
if [ "$KIT" = "$DEST" ]; then
  echo "Run this from your workspace root: sh $KIT/install.sh" >&2
  exit 1
fi

copied=0
kept=0
# shortcut: word-splits on spaces, fine because every kit path is space-free; switch to find -exec if that changes.
for rel in $(cd "$KIT" && find .agents/skills .codex/agents -type f); do
  if [ -e "$DEST/$rel" ]; then
    kept=$((kept + 1))
  else
    mkdir -p "$(dirname "$DEST/$rel")"
    cp "$KIT/$rel" "$DEST/$rel"
    copied=$((copied + 1))
  fi
done

MARK='<!-- codex-lean-kit -->'
if [ ! -e "$DEST/AGENTS.md" ]; then
  cp "$KIT/AGENTS.md" "$DEST/AGENTS.md"
  echo "AGENTS.md: created"
elif grep -qF "$MARK" "$DEST/AGENTS.md"; then
  echo "AGENTS.md: kit section already present"
else
  printf '\n' >> "$DEST/AGENTS.md"
  cat "$KIT/AGENTS.md" >> "$DEST/AGENTS.md"
  echo "AGENTS.md: kit section appended below the existing content"
fi

echo "files copied: $copied, existing kept: $kept"
echo "skills: $(ls "$DEST/.agents/skills" | tr '\n' ' ')"
for f in "$DEST"/.codex/agents/*.toml; do
  echo "role $(basename "$f" .toml) -> $(sed -n 's/^model *= *"\(.*\)"/\1/p' "$f")"
done
echo "next:  codex -m gpt-6.1-sol -c model_reasoning_effort=\"medium\" --disable computer_use --disable browser_use"
echo "       choose 'trust' when asked; roles in .codex/agents load only in a trusted folder."
echo "check: codex debug prompt-input -c 'model=\"gpt-6.1-sol\"' hi | grep -c 'Available roles'   (1 = roles loaded, no tokens used)"
echo "if 0:  mkdir -p ~/.codex/agents && cp .codex/agents/*.toml ~/.codex/agents/   (user-level roles load without trust)"
