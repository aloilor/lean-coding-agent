# Honor Bootstrap Installation Scope

## Mistake Pattern

I treated a project-initialization request as config/docs-only, then as conditional on an existing `package.json`, even though the user wanted initialized projects to receive the actual installed tooling.

## Rule

When the user asks to install tooling in initialized projects, make the bootstrap perform the installation and create any required project metadata unless they explicitly ask for documentation-only behavior. If the installation tool uses a different layout than this repo expects, bridge the layouts in the bootstrap and verify the generated target files.
