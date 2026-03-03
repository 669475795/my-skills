# Agent Rules

## Encoding-Safe Editing

- For any file containing Chinese text or unclear encoding, inspect encoding and BOM before editing.
- Prefer minimal patches over full-file rewrites.
- After edits, verify both raw bytes and rendered text for the changed areas.
- Never assume UTF-8 without checking first.
