import { expect, test } from "./fixtures";

test("the home page editor reformats the template and goes back", async ({ page }) => {
  await page.goto("/");
  const editor = page.getByRole("figure").filter({ hasText: "messy.html" });
  const run = editor.getByRole("button", { name: /--reformat/ });
  const problems = await editor.locator("mark").count();
  expect(problems).toBeGreaterThan(0);

  const code = editor.locator("pre:visible");
  const messy = async () => {
    await expect(editor.getByText(`${problems} problems`)).toBeVisible();
    await expect(code).toContainText("{%if posts%}");
  };
  await messy();

  await run.click();
  await expect(editor.getByText("No problems")).toBeVisible();
  await expect(editor.getByText(`${problems} problems`)).toBeHidden();
  await expect(code).toContainText("{% if posts %}");

  await run.click();
  await messy();
});

test("the home page menu lists what the docs sidebar does", async ({ page }) => {
  // Narrower than the header's section links, where the menu button shows.
  await page.setViewportSize({ width: 1000, height: 800 });
  const links = (selector: string) =>
    page.locator(`${selector} a`).evaluateAll((all) => all.map((a) => a.getAttribute("href")));

  await page.goto("/docs/getting-started/");
  const sidebar = await links("#starlight__sidebar .sidebar-content");
  expect(sidebar.length).toBeGreaterThan(10);

  await page.goto("/");
  await page.getByRole("button", { name: "Menu" }).click();
  await expect(page.locator("#dj-menu")).toBeVisible();
  expect(await links("#dj-menu")).toEqual(sidebar);
});
