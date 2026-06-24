# Do Not Run Startup Skill Update Automatically

## Mistake Pattern

Running the project skill update command automatically at session startup can create unnecessary churn when the user expects a quiet start.

## Rule

Do not run `skills update --project --yes` merely because `skills-lock.json` exists. Run it only when the user asks for a skill update or the active task directly requires syncing project skills, then report any resulting file changes or failures.
