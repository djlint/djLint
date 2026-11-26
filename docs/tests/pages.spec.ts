import { AxeBuilder } from "@axe-core/playwright";

import { MISSING, expect, test } from "./fixtures";

const PAGES = [
  "/",
  "/docs/getting-started/",
  "/docs/configuration/",
  "/docs/linter/",
  "/docs/integrations/",
  "/docs/changelog/",
  "/demo/",
  "/ru/",
  MISSING,
];

// Starlight's search button shows its Ctrl K shortcut, which the button's name,
// "Search", leaves out. Starlight counts the shortcut as a hint rather than
// part of the label and keeps it (withastro/starlight#4260).
const upstream = (rule: string, html: string) =>
  rule === "label-content-name-mismatch" && html.startsWith("<button data-open-modal");

// axe takes over 30 seconds on these on a CI runner, against under 10 here.
const LONG = new Set(["/docs/configuration/", "/docs/linter/", "/docs/changelog/"]);

for (const path of PAGES) {
  test(`${path} fits the window and passes axe`, async ({ page }) => {
    test.slow(LONG.has(path), "a long page");
    await page.goto(path);
    // The web fonts are wider than the fallbacks.
    await page.evaluate(async () => {
      await document.fonts.ready;
    });

    // Anything wider than the window, outside a box that scrolls or clips it.
    const overflow = await page.evaluate(() => {
      const width = document.documentElement.clientWidth;
      const clipped = (element: Element) => {
        for (let parent = element.parentElement; parent; parent = parent.parentElement) {
          if (parent === document.body) {
            return false;
          }
          if (getComputedStyle(parent).overflowX !== "visible") {
            return true;
          }
        }
        return false;
      };
      const wide = [...document.body.querySelectorAll("*")]
        .filter((element) => element.getBoundingClientRect().right > width + 1)
        .filter((element) => !clipped(element) && element.checkVisibility())
        .slice(0, 5)
        .map((element) => element.outerHTML.slice(0, 120));
      return { scrollWidth: document.documentElement.scrollWidth, width, wide };
    });
    expect(overflow.scrollWidth, `wider than the window: ${overflow.wide.join("\n")}`).toBe(
      overflow.width,
    );

    // Expressive Code makes a code block that scrolls focusable a moment after
    // it lays out; axe would find the ones it hasn't reached yet.
    await expect
      .poll(async () =>
        page.evaluate(
          () =>
            [...document.querySelectorAll(".expressive-code pre")].filter(
              (pre) => pre.scrollWidth > pre.clientWidth && !pre.hasAttribute("tabindex"),
            ).length,
        ),
      )
      .toBe(0);

    // Every rule in the light theme, and the one that depends on the colors in
    // the dark theme too.
    for (const theme of ["light", "dark"] as const) {
      await page.emulateMedia({ colorScheme: theme });
      await expect(page.locator("html")).toHaveAttribute("data-theme", theme);
      const axe = new AxeBuilder({ page });
      if (theme === "dark") {
        axe.withRules(["color-contrast"]);
      }
      // Expressive Code gives every code block that scrolls role="region" with
      // no label of its own, so a page with several fails this best-practice
      // rule; it is Expressive Code's to fix, not the page's.
      else {
        axe.disableRules(["landmark-unique"]);
      }
      const { violations } = await axe.analyze();
      const found = violations.flatMap(({ id, nodes }) =>
        nodes
          .filter(({ html }) => !upstream(id, html))
          .map(({ target }) => `${id}: ${target.join(" ")}`),
      );
      expect(found, `axe in the ${theme} theme`).toEqual([]);
    }
  });
}

test("the 404 page links back to the docs", async ({ page }) => {
  const response = await page.goto(MISSING);
  expect(response?.status()).toBe(404);
  const main = page.getByRole("main");
  await expect(main.getByRole("heading", { level: 1 })).toHaveText("404");
  await expect(main.getByRole("link", { name: "Getting started" })).toHaveAttribute(
    "href",
    "/docs/getting-started/",
  );
  await expect(main.getByRole("link", { name: "Configuration" })).toHaveAttribute(
    "href",
    "/docs/configuration/",
  );
  await expect(main.getByRole("link", { name: "Home" })).toHaveAttribute("href", "/");
});
