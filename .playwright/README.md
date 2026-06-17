# Playwright CLI

This folder contains the project-local Playwright CLI config copied by the shared agent bootstrap.

The shared bootstrap installs the CLI as a dev dependency. To install or refresh it manually, run:

```bash
npm install --save-dev @playwright/cli@latest
```

Then run it through the project-local package:

```bash
npx playwright-cli --help
npx playwright-cli config-print
npx playwright-cli open http://localhost:3000 --headed
```

The CLI automatically loads `.playwright/cli.config.json` when present.
