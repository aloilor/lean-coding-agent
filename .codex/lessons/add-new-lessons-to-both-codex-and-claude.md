# Add New Lessons To Both Codex And Claude

## Mistake Pattern

I treated lessons as tool-local and added a new lesson in only one tree, leaving the other supported tool without the same reusable correction.

## Rule

Whenever I add a new lesson in this repo, create the same lesson file in both `.codex/lessons/` and `.claude/lessons/`, and update both `LESSONS.md` indexes in the same pass.
