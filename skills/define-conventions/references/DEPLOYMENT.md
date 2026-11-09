# Deployment Grill Guide

Find out how code reaches users and what can go wrong on the way. Most of this cannot be inferred from a repo, and it is where a wrong guess costs the most. If the project is not deployed, confirm that with one question and skip this file.

Examples below show the shape of a useful line. Never copy them into a project.

## Environments

- **Ask about:** which environments exist (local, preview, stage, prod), their URLs, what data each holds, how they differ from each other.
- **Look at:** infrastructure as code, CI deploy jobs, environment config files.
- Public URLs can be recorded. Ask before recording internal hostnames, account IDs, or non-public URLs, and offer `AGENTS.override.md` instead.
- Useful: "Stage is `https://stage.example.com` and holds anonymized prod data, refreshed weekly."

## How Deploys Happen

- **Ask about:** what triggers a deploy, who can approve prod, freeze windows, the order services must go out in, where config and secrets are set (names only).
- **Look at:** deploy workflows, release scripts, `Procfile`, Helm charts, Terraform.
- Useful: "Merging to `main` deploys to stage automatically; prod needs a manual approval in the deploy workflow."
- Obvious: "Deploys are automated with CI."

## Migrations

- **Ask about:** when migrations run relative to the deploy, backward-compatibility requirements, rollout of destructive changes.
- **Look at:** migration directories and history, deploy steps that run them.
- Useful: "Migrations must work with the previous release; drop columns one release after the code stops using them."

## Rollback, Hotfixes, And Incidents

- **Ask about:** how to roll back and what cannot be rolled back, the hotfix path, what to do during an incident, who to tell.
- **Look at:** hotfix branches and tags in git history, `docs/incidents/`.
- Useful: "Roll back by redeploying the previous tag; migrations are forward-only, so ship a fix instead when one ran."

## Feature Flags

Only when the project uses them.

- **Ask about:** when a flag is required, where flags are defined, who removes them and when.

## Observability

- **Ask about:** where logs, metrics, and alerts live, what a new feature must emit.
- **Look at:** logging and metrics setup, dashboards as code.
- Useful: "New background jobs must emit `job.duration` and `job.failed`."

## What Agents May Do Alone

Always ask this. It carries the most risk of anything in these files.

- **Ask about:** deploying to each environment, running migrations, reading or changing prod data, changing infrastructure or secrets.
- Useful: "Agents may deploy to stage. Agents never deploy to prod or run migrations against it."
