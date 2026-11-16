// The demo's settings as djLint takes them, without a browser.
import { expect, test } from "@playwright/test";

import { apiOptions, commands, configFile, isSet } from "../src/scripts/demo-config";

const CONFIG = {
  profile: "jinja",
  indent: "2",
  indent_css: "3",
  custom_html: "mj-\\w+",
  blank_line_after_tag: "load,extends",
  format_css: true,
};

test("API options turn the numbers into numbers", () => {
  expect(apiOptions(CONFIG)).toEqual({ ...CONFIG, indent: 2, indent_css: 3 });
});

test("commands quote what the shell would split or expand", () => {
  expect(commands({})).toBe("djlint input.html --reformat\ndjlint input.html --lint");
  expect(commands({ custom_html: "it's", format_css: true }).split("\n")[0]).toBe(
    "djlint input.html --reformat --custom-html='it'\\''s' --format-css",
  );
  expect(commands(CONFIG).split("\n")[1]).toBe(
    "djlint input.html --lint --profile=jinja --indent=2 --indent-css=3 --custom-html='mj-\\w+' --blank-line-after-tag=load,extends --format-css",
  );
});

test("config files take lists and put the CSS and JS indents in their own tables", () => {
  expect(configFile(CONFIG, "pyproject.toml")).toBe(
    [
      "[tool.djlint]",
      'profile = "jinja"',
      "indent = 2",
      "custom_html = ['mj-\\w+']",
      'blank_line_after_tag = ["load", "extends"]',
      "format_css = true",
      "",
      "[tool.djlint.css]",
      "indent_size = 3",
    ].join("\n"),
  );
  expect(configFile({ indent_js: "2" }, "djlint.toml")).toBe("[js]\nindent_size = 2");
  expect(JSON.parse(configFile(CONFIG, ".djlintrc"))).toEqual({
    profile: "jinja",
    indent: 2,
    custom_html: ["mj-\\w+"],
    blank_line_after_tag: ["load", "extends"],
    format_css: true,
    css: { indent_size: 3 },
  });
  expect(configFile({}, "pyproject.toml")).toBe("");
});

test("a 0 that djLint reads as unset is left out", () => {
  expect(isSet("indent", "0")).toBe(false);
  expect(isSet("max_line_length", "0")).toBe(false);
  expect(isSet("max_blank_lines", "0")).toBe(true);
  expect(isSet("indent", "2")).toBe(true);
  expect(isSet("format_css", false)).toBe(false);
});
