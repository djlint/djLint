import { expect, test as base } from "@playwright/test";

export { expect } from "@playwright/test";

/** An address with no page behind it: the browser logs its 404, which is expected. */
export const MISSING = "/no-such-page/";

// Every test fails on an uncaught error or a console error in the page.
export const test = base.extend<{ pageErrors: string[] }>({
  pageErrors: [
    async ({ page }, use) => {
      const errors: string[] = [];
      page.on("pageerror", (error) => errors.push(`${error.name}: ${error.message}`));
      page.on("console", (message) => {
        if (message.type() !== "error") {
          return;
        }
        if (new URL(message.location().url || "about:blank").pathname === MISSING) {
          return;
        }
        errors.push(`console: ${message.text()} (${message.location().url})`);
      });
      await use(errors);
      expect(errors, "errors in the page").toEqual([]);
    },
    { auto: true },
  ],
});
