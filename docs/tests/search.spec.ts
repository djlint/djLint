import { expect, test } from "./fixtures";

test("Ctrl+K opens the search, which finds an option", async ({ page }) => {
  await page.goto("/docs/getting-started/");
  await expect(page.getByRole("button", { name: "Search" })).toBeEnabled();
  await page.keyboard.press("Control+k");
  const dialog = page.getByRole("dialog", { name: "Search" });
  await expect(dialog).toBeVisible();
  await dialog.getByRole("textbox", { name: "Search" }).fill("max_line_length");
  // The page's own result comes first; a match in its intro adds one for #_top below it.
  await expect(
    dialog.getByRole("link", { name: "Configuration", exact: true }).first(),
  ).toHaveAttribute("href", "/docs/configuration/");
});
