import options from "../src/data/configuration.json" with { type: "json" };
import { expect, test } from "./fixtures";

const ids = options.map(({ name }) => name.replaceAll("_", "-")).toSorted();

test.beforeEach(async ({ page }) => {
  await page.goto("/docs/configuration/");
});

test("every option has its section and an entry in the table of contents", async ({ page }) => {
  const sections = page.getByRole("main").getByRole("heading", { level: 3 });
  expect((await sections.evaluateAll((all) => all.map(({ id }) => id))).toSorted()).toEqual(ids);

  const toc = page.getByRole("navigation", { name: "On this page" });
  const hrefs = await toc
    .getByRole("link")
    .evaluateAll((all) => all.map((a) => a.getAttribute("href")));
  expect(hrefs).toEqual(expect.arrayContaining(ids.map((id) => `#${id}`)));
});

test("the filter hides the options that don't match", async ({ page }) => {
  const filter = page.getByRole("searchbox", { name: "Filter options" });
  const visible = page.getByRole("main").getByRole("heading", { level: 3 });

  await filter.fill("max_line_length");
  await expect(visible.first()).toHaveText("max_line_length");
  await expect(page.getByRole("heading", { name: "indent", exact: true })).toBeHidden();
  expect(await visible.count()).toBeLessThan(ids.length);

  await filter.fill("zzz");
  await expect(page.getByText("Nothing found. Try another search.")).toBeVisible();
  await expect(visible).toHaveCount(0);

  await filter.fill("");
  await expect(visible).toHaveCount(ids.length);
});
