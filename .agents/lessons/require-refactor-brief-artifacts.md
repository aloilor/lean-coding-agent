# Require Refactor Brief Artifacts

## Mistake Pattern

Treating refactor planning as a sidebar to feature specification work can let refactors proceed without a saved behavior-preservation contract or implementation plan.

## Rule

For planned refactors, keep a distinct refactor planning workflow instead of folding refactors into feature-specification flow. Require a saved refactor brief and matching implementation plan before implementation starts. The brief should define behavior to preserve, scope boundaries, verification checks, behavior-drift risks, rollback risks, and required refactor/testing/SQL skills.
