import type { Locator, Page } from "@playwright/test";

import { expect, test } from "./fixtures";

const WELCOME = "<div>\n    <p>Welcome to djLint online!</p>\n</div>";
const MESSY = "<ul>\n<li>{%if a%}<img src='a.png'>{%endif%}</li>\n<li>\n{{b}}\n</li>\n</ul>";
// What `djlint - --reformat` makes of it, with and without --indent=2. Linting
// finds H008 and H013 in it.
const formatted = (indent: string) =>
  [
    "<ul>",
    `${indent}<li>`,
    `${indent.repeat(2)}{% if a %}<img src="a.png">{% endif %}`,
    `${indent}</li>`,
    `${indent}<li>{{ b }}</li>`,
    "</ul>",
  ].join("\n");

const text = async (view: Locator) => (await view.locator(".cm-line").allTextContents()).join("\n");

const demo = (page: Page) => ({
  input: page.getByRole("textbox", { name: "input.html", exact: true }),
  // The output editor is labelled by the view it shows.
  output: page.locator("#djlint-output").getByRole("textbox"),
  problems: page.locator("#djlint-problems"),
  indent: page.getByRole("spinbutton", { name: "Indent", exact: true }),
  view: (name: string) => page.getByRole("button", { name, exact: true }),
});

// One test, so Pyodide comes from the CDN once (the reload hits the cache).
test("the demo formats, lints, takes settings and restores them from the address", async ({
  page,
}) => {
  test.slow();
  await page.goto("/demo/");
  const { input, output, problems, indent, view } = demo(page);

  await test.step("djLint loads, formats the welcome example and fills the window", async () => {
    await expect(page.locator("#djlint-version")).not.toBeEmpty({ timeout: 60_000 });
    await expect.poll(async () => text(output)).toBe(WELCOME);
    await expect(page.locator(".demo-loading")).toBeHidden();
    await expect(problems).toHaveText("No problems");
    expect(new URL(page.url()).hash).toBe("");
    // The page doesn't scroll, and the editors reach down to its bottom padding.
    const size = await page.evaluate(() => ({
      height: document.documentElement.scrollHeight,
      width: document.documentElement.scrollWidth,
    }));
    expect(size).toEqual(page.viewportSize());
    const gap = await page
      .locator(".demo-workspace")
      .evaluate((workspace) => innerHeight - workspace.getBoundingClientRect().bottom);
    expect(gap).toBeLessThanOrEqual(48);
  });

  await test.step("a template is formatted and linted", async () => {
    await input.fill(MESSY);
    await expect.poll(async () => text(output)).toBe(formatted("    "));
    await expect(problems).toHaveText("Problems: 2");
    await expect(input.locator(".cm-lintRange")).toHaveCount(2);
  });

  await test.step("a setting changes the output, the commands and the config files", async () => {
    await indent.fill("2");
    await expect.poll(async () => text(output)).toBe(formatted("  "));

    await view("CLI").click();
    await expect(view("CLI")).toHaveAttribute("aria-pressed", "true");
    await expect
      .poll(async () => text(output))
      .toBe("djlint input.html --reformat --indent=2\ndjlint input.html --lint --indent=2");
    await view("pyproject.toml").click();
    await expect.poll(async () => text(output)).toBe("[tool.djlint]\nindent = 2");
    await view("Output").click();
    await expect.poll(async () => text(output)).toBe(formatted("  "));
    await expect.poll(() => new URL(page.url()).hash.length).toBeGreaterThan(1);
  });

  await test.step("an indent of 0, which djLint reads as unset, is unset everywhere", async () => {
    await indent.fill("0");
    await expect.poll(async () => text(output)).toBe(formatted("    "));
    await view("CLI").click();
    await expect
      .poll(async () => text(output))
      .toBe("djlint input.html --reformat\ndjlint input.html --lint");
    await view("pyproject.toml").click();
    await expect.poll(async () => text(output)).toMatch(/^# /u);
    await view("Output").click();
    await indent.fill("2");
    await expect.poll(async () => text(output)).toBe(formatted("  "));
  });

  await test.step("a setting djLint warns about shows the warning, every time", async () => {
    const include = page.getByRole("textbox", { name: "Rules to add", exact: true });
    const warnings = page.locator("#djlint-warnings");
    await include.fill("X999");
    await expect(warnings).toHaveText("include names X999, which is not a linter rule.");
    await include.fill("");
    await expect(warnings).toBeEmpty();
    // A second run with the same setting warns again.
    await include.fill("X999");
    await expect(warnings).toHaveText("include names X999, which is not a linter rule.");
    await include.fill("");
    await expect(warnings).toBeEmpty();
  });

  await test.step("the address brings back the example and its settings", async () => {
    await page.reload();
    await expect.poll(async () => text(input)).toBe(MESSY);
    await expect(indent).toHaveValue("2");
    await expect.poll(async () => text(output), { timeout: 60_000 }).toBe(formatted("  "));
    await expect(problems).toHaveText("Problems: 2");
  });
});
