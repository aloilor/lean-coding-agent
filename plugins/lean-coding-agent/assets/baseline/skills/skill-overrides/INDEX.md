# Skill Overrides

Shared baseline overrides for installed skills live here. The bootstrap copies these files into each target repo's `.agents/skill-overrides/` directory so agents can apply them without editing installed upstream skills.

Before running a skill, check `.agents/skill-overrides/INDEX.md` in the target repo. If the skill is listed below, read `.agents/skill-overrides/<skill-name>.md` and apply it. These overrides extend installed skills; when an override conflicts with the skill's default behavior, the override wins.

- [create-specification](create-specification.md) - save specifications under `docs/spec/` instead of the default `/spec/`.
- [prd](prd.md) - save PRDs under `docs/prd/` as `prd-<name>.md`.
- [tdd](tdd.md) - enforce repo-aware, assertion-red TDD with reliable behavior tests; also carries this repo's test-strategy, doubles, and testable-design guidance.
