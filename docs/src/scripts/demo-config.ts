// The demo's settings as djLint takes them: options for its Python API, the
// commands that do the same, and the configuration files that set them.

/** The form's values by option name: text as typed, switches as true. */
export type DemoConfig = Record<string, string | boolean>;

const NUMBERS = new Set([
  "format_attribute_js_json_min_props",
  "indent",
  "indent_css",
  "indent_js",
  "max_attribute_length",
  "max_blank_lines",
  "max_line_length",
]);

// Comma-separated on the command line, lists in a configuration file.
const LISTS = new Set([
  "blank_line_after_tag",
  "blank_line_before_tag",
  "custom_blocks",
  "custom_html",
  "ignore",
  "ignore_blocks",
  "include",
]);

// --indent-css and --indent-js are indent_size in the css and js tables of a
// configuration file.
const TABLES: Record<string, string> = { indent_css: "css", indent_js: "js" };

function typed(name: string, value: string | boolean): string | number | boolean {
  return typeof value === "string" && NUMBERS.has(name) ? Number(value) : value;
}

// The command line and the API of djLint read 0 for these as "not set",
// but a configuration file would set 0, so the demo leaves a 0 out.
const ZERO_IS_UNSET = new Set(["indent", "indent_css", "indent_js", "max_line_length"]);

/**
 * Whether a form value sets anything.
 * @param name - The option's name.
 * @param value - Its value in the form.
 * @returns False for an empty field, a switch that is off and a 0 that means "not set".
 */
export function isSet(name: string, value: string | boolean): boolean {
  return Boolean(value) && !(ZERO_IS_UNSET.has(name) && Number(value) === 0);
}

/**
 * The settings for djLint's Python API.
 * @param config - The form's values.
 * @returns Keyword arguments for djlint.api.load_config.
 */
export function apiOptions(config: DemoConfig): Record<string, string | number | boolean> {
  return Object.fromEntries(
    Object.entries(config).map(([name, value]) => [name, typed(name, value)]),
  );
}

function shellWord(text: string): string {
  return /^[\w,.+-]+$/u.test(text) ? text : `'${text.replaceAll("'", String.raw`'\''`)}'`;
}

/**
 * The commands that do what the demo does.
 * @param config - The form's values.
 * @returns The commands that format and lint input.html with these settings.
 */
export function commands(config: DemoConfig): string {
  const flags = Object.entries(config).map(([name, value]) => {
    const flag = `--${name.replaceAll("_", "-")}`;
    return typeof value === "string" ? `${flag}=${shellWord(value)}` : flag;
  });
  return ["--reformat", "--lint"]
    .map((mode) => ["djlint input.html", mode, ...flags].join(" "))
    .join("\n");
}

type Value = string | number | boolean | string[];

function tomlValue(value: Value): string {
  if (Array.isArray(value)) {
    return `[${value.map((item) => tomlValue(item)).join(", ")}]`;
  }
  if (typeof value !== "string") {
    return String(value);
  }
  // A literal string keeps the backslashes of a regex as they are.
  if (/["\\]/u.test(value) && !value.includes("'")) {
    return `'${value}'`;
  }
  return JSON.stringify(value);
}

function tomlLines(values: Record<string, Value>): string[] {
  return Object.entries(values).map(([name, value]) => `${name} = ${tomlValue(value)}`);
}

function fileValue(name: string, value: string | boolean): Value {
  return typeof value === "string" && LISTS.has(name)
    ? value
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean)
    : typed(name, value);
}

/**
 * A configuration file with the demo's settings.
 * @param config - The form's values.
 * @param file - The file's name, which sets its format.
 * @returns The file's text, or an empty string when nothing is set.
 */
export function configFile(
  config: DemoConfig,
  file: "pyproject.toml" | "djlint.toml" | ".djlintrc",
): string {
  const top: Record<string, Value> = {};
  const tables: Record<string, Record<string, number>> = {};
  for (const [name, value] of Object.entries(config)) {
    const table = TABLES[name];
    if (table) {
      tables[table] = { indent_size: Number(value) };
    } else {
      top[name] = fileValue(name, value);
    }
  }
  if (file === ".djlintrc") {
    return JSON.stringify({ ...top, ...tables }, null, 2);
  }

  const prefix = file === "pyproject.toml" ? "tool.djlint" : "";
  const sections: string[] = [];
  if (Object.keys(top).length) {
    const lines = tomlLines(top);
    sections.push((prefix ? [`[${prefix}]`, ...lines] : lines).join("\n"));
  }
  for (const [table, values] of Object.entries(tables)) {
    sections.push([`[${prefix ? `${prefix}.` : ""}${table}]`, ...tomlLines(values)].join("\n"));
  }
  return sections.join("\n\n");
}
