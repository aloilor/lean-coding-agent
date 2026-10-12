# Honor Setup Installation Scope

## Mistake Pattern

I treated a project-setup request as config/docs-only, then as conditional on an existing `package.json`, even though the user wanted set-up projects to receive the actual installed tooling.

## Rule

When the user asks to install tooling in set-up projects, make the setup script perform the installation and create any required project metadata unless they explicitly ask for documentation-only behavior. If the installation tool uses a different layout than this repo expects, bridge the layouts in the setup script and verify the generated target files.
