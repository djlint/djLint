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
