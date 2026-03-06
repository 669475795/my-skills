# AGENTS.md

## Objective

- Default to end-to-end execution for coding tasks in this repository.
- Minimize user interruptions during large, multi-file work.
- Prefer reasonable assumptions over confirmation loops.

## Execution Policy

- Execute the most reasonable path without intermediate confirmation.
- Do not stop at analysis or planning unless the user explicitly asks for that.
- For implementation requests, complete the full loop when feasible: inspect, design, edit, validate, report.
- Ask the user only if the requirement is materially ambiguous, the action is destructive, secrets or production access are required, or the environment blocks safe execution.

## Autonomous Workflow

- For substantial tasks, automatically search relevant files, configs, tests, and entry points before editing.
- Perform requirement analysis and impact analysis before code changes.
- Prefer targeted search and progressive disclosure over reading the whole repository.
- Continue through related subtasks until the requested outcome is complete.
- Run the most relevant tests, linters, or compile checks after changes.
- Review the final diff before finishing.

## Auto Commit Policy

- Auto-commit is allowed for self-contained tasks with validated changes.
- Do not commit if the worktree contains unrelated user changes, failing tests, or unresolved ambiguity.
- Never amend existing commits unless explicitly requested.
- Never include unrelated files in an automatic commit.
- Use a concise commit message that matches repository conventions.

## Approval Minimization

- Prefer commands and workflows that stay inside the current workspace.
- Batch related reads, edits, and validations to reduce back-and-forth.
- If a command fails because of shell profile or wrapper issues, try a simpler equivalent first.
- Document low-risk assumptions in the final report instead of interrupting execution.

## Coding Workflow

- Build context from the codebase first. Do not infer architecture from filenames alone.
- Prefer targeted inspection over broad file dumps.
- Favor minimal patches over large rewrites.
- Preserve existing patterns unless clearly broken or the user asks for a refactor.
- Run the smallest focused validation that can prove the change.

## Safety Boundaries

- Never run destructive repository operations unless the user explicitly requests them.
- Never revert user changes you did not make unless explicitly instructed.
- Do not modify files outside scope unless required to keep the build or tests consistent.
- Flag risky migrations, schema changes, infrastructure changes, or contract changes before applying them.

## Windows And Encoding

- On Windows, prefer shell invocations that avoid broken profile initialization when possible.
- Before editing files that may contain Chinese text or uncertain encoding, inspect encoding and BOM first.
- Prefer minimal patches for encoding-sensitive files.
- After editing encoding-sensitive content, verify both bytes and rendered text for the changed area.

## macOS And Unix

- On macOS, prefer shell invocations that avoid interactive shell startup files when possible.
- Prefer zsh or bash with no profile or rc loading for automation.
- Use POSIX-safe paths and quoting for commands that may run on macOS or Linux.
- Prefer repository-local tools and pinned environments over machine-global packages.
- Avoid commands that require GUI confirmation or Keychain access unless explicitly requested.

## Repository-Specific Default

- Optimize for autonomous execution with minimal approvals and minimal clarification turns.
