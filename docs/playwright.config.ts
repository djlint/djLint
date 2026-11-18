import { defineConfig, devices } from "@playwright/test";

// Not 4321, where `astro dev` and other previews of the site tend to run already.
const PORT = 4327;
const CI = Boolean(process.env["CI"]);

// Checks the built site in dist/ (`npm run build` first), so a dependency
// update that breaks a page fails CI before Renovate merges it.
export default defineConfig({
  forbidOnly: CI,
  fullyParallel: true,
  projects: [
    {
      name: "desktop",
      use: { ...devices["Desktop Chrome"], viewport: { height: 900, width: 1440 } },
    },
    // A phone only for the checks that every page passes; the rest is the same
    // code at any width.
    {
      name: "phone",
      testMatch: "pages.spec.ts",
      use: { ...devices["Pixel 7"], viewport: { height: 844, width: 390 } },
    },
  ],
  reporter: CI ? [["github"], ["list"]] : "list",
  // The demo loads Pyodide from the CDN, which can hiccup.
  retries: CI ? 1 : 0,
  testDir: "tests",
  use: {
    baseURL: `http://localhost:${PORT}`,
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  webServer: {
    command: `npx astro preview --port ${PORT}`,
    reuseExistingServer: !CI,
    url: `http://localhost:${PORT}/`,
  },
  workers: 4,
});
