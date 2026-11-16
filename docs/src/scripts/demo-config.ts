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

// --indent-css and --indent-js are indent_size in the css and js tables of a
// configuration file.
const TABLES: Record<string, string> = { indent_css: "css", indent_js: "js" };

const typed = (name: string, value: string | boolean) =>
  typeof value === "string" && NUMBERS.has(name) ? Number(value) : value;

/** Keyword arguments for djlint.api.load_config. */
export const apiOptions = (config: DemoConfig) =>
  Object.fromEntries(Object.entries(config).map(([name, value]) => [name, typed(name, value)]));

const shellWord = (text: string) =>
  /^[\w,.+-]+$/.test(text) ? text : `'${text.replaceAll("'", "'\\''")}'`;

/** The commands that format and lint input.html with these settings. */
export function commands(config: DemoConfig) {
  const flags = Object.entries(config).map(([name, value]) => {
    const flag = `--${name.replaceAll("_", "-")}`;
    return value === true ? flag : `${flag}=${shellWord(value)}`;
  });
  return ["--reformat", "--lint"]
    .map((mode) => ["djlint input.html", mode, ...flags].join(" "))
    .join("\n");
}

const tomlValue = (value: string | number | boolean) => {
  if (typeof value !== "string") return String(value);
  // A literal string keeps the backslashes of a regex as they are.
  if (/["\\]/.test(value) && !value.includes("'")) return `'${value}'`;
  return JSON.stringify(value);
};

/** One configuration file with these settings, or an empty string when none are set. */
export function configFile(
  config: DemoConfig,
  file: "pyproject.toml" | "djlint.toml" | ".djlintrc",
) {
  const top: Record<string, string | number | boolean> = {};
  const tables: Record<string, Record<string, number>> = {};
  for (const [name, value] of Object.entries(config)) {
    const table = TABLES[name];
    if (table) tables[table] = { indent_size: Number(value) };
    else top[name] = typed(name, value);
  }
  if (file === ".djlintrc") return JSON.stringify({ ...top, ...tables }, null, 2);

  const prefix = file === "pyproject.toml" ? "tool.djlint" : "";
  const lines = (values: object) =>
    Object.entries(values).map(([name, value]) => `${name} = ${tomlValue(value)}`);
  const sections = [
    [...(prefix && Object.keys(top).length ? [`[${prefix}]`] : []), ...lines(top)],
    ...Object.entries(tables).map(([table, values]) => [
      `[${prefix ? `${prefix}.` : ""}${table}]`,
      ...lines(values),
    ]),
  ].filter((section) => section.length);
  return sections.map((section) => section.join("\n")).join("\n\n");
}
