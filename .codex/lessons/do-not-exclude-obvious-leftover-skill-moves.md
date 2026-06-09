# Do Not Exclude Obvious Leftover Skill Moves

## Mistake Pattern

I stopped a commit run while tracked skill folders had been deleted from `global-skills/` and matching replacements were sitting untracked under `.codex/skills/`, even though that clearly represented an intended move.

## Rule

When deleted tracked files and matching untracked replacements clearly form one intended move, treat that as remaining requested work and commit it instead of excluding it as unrelated leftover state.
