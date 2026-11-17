import { expect, test } from "./fixtures";

// Links from before the move to Starlight, still out there in issues, answers
// and READMEs.
for (const [path, target] of [
  ["/docs/configuration/#max-line-length", "max_line_length"],
  ["/docs/linter/#h006", "H006"],
]) {
  test(`${path} still lands on its section`, async ({ page }) => {
    const response = await page.goto(path);
    expect(response?.ok()).toBe(true);
    const id = new URL(path, "http://localhost").hash.slice(1);
    const heading = page.locator(`[id="${id}"]`);
    await expect(heading).toContainText(target);
    await expect(heading).toBeInViewport();
  });
}

test("translated pages keep their address", async ({ page }) => {
  const response = await page.goto("/ru/docs/configuration/");
  expect(response?.ok()).toBe(true);
  await expect(page.locator("html")).toHaveAttribute("lang", "ru");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Конфигурация");
});

// Files other projects load from the site: the README logos, the MegaLinter
// banner, the JSON schema SchemaStore points to.
for (const path of [
  "/static/img/icon.png",
  "/static/img/logo-wide-dark.svg",
  "/static/img/logo-wide-light.svg",
  "/schema/djlint.json",
]) {
  test(`${path} is still served`, async ({ request }) => {
    expect((await request.get(path)).ok()).toBe(true);
  });
}
