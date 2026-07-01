# Skill Overrides

Project-specific overrides that adjust the default behavior of installed skills without editing the skills themselves. Installed and marketplace skills are overwritten when they update, so overrides live here instead. These files are shared (committed), unlike the private `*.local.md` files.

Before running a skill, check this index. If the skill is listed below, read `.agents/skill-overrides/<skill-name>.md` and apply it — those overrides take precedence over that skill's default behavior.

One file per overridden skill, named `<skill-name>.md` to match the skill's name. Add a matching clickable entry here whenever you add an override.

- [create-specification](create-specification.md) — save specifications under `docs/spec/` instead of the default `/spec/`.
- [prd](prd.md) — save PRDs under `docs/prd/` as `prd-<name>.md`.
