import { defineConfig, devices } from "@playwright/test";

// Not 4321, where `astro dev` and other previews of the site tend to run already.
const PORT = 4327;

// Checks the built site in dist/ (`npm run build` first), so a dependency
// update that breaks a page fails CI before Renovate merges it.
export default defineConfig({
  testDir: "tests",
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  // The demo loads Pyodide from the CDN, which can hiccup.
  retries: process.env.CI ? 1 : 0,
  workers: 4,
  reporter: process.env.CI ? [["github"], ["list"]] : "list",
  use: {
    baseURL: `http://localhost:${PORT}`,
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "desktop",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1440, height: 900 } },
    },
    // A phone only for the checks that every page passes; the rest is the same
    // code at any width.
    {
      name: "phone",
      testMatch: "pages.spec.ts",
      use: { ...devices["Pixel 7"], viewport: { width: 390, height: 844 } },
    },
  ],
  webServer: {
    command: `npx astro preview --port ${PORT}`,
    url: `http://localhost:${PORT}/`,
    reuseExistingServer: !process.env.CI,
  },
});
