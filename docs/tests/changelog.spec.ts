import { expect, test } from "./fixtures";

// The ids the old site gave the releases, which links out there still use.
const RELEASES = { "1504": "1.50.4", "100": "1.0.0", "059a": "0.5.9a" };

test("releases keep their old anchors and are listed in the table of contents", async ({
  page,
}) => {
  await page.goto("/docs/changelog/");
  const toc = page.getByRole("navigation", { name: "On this page" });
  for (const [id, version] of Object.entries(RELEASES)) {
    await expect(page.locator(`h2[id="${id}"]`)).toContainText(version);
    await expect(toc.locator(`a[href="#${id}"]`)).toHaveText(version);
  }
});
