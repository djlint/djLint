/**
 * @type {import('prettier').Config & import("@ianvs/prettier-plugin-sort-imports").PluginConfig}
 */
export default {
  objectWrap: "collapse",
  plugins: [
    "@ianvs/prettier-plugin-sort-imports",
    "prettier-plugin-packagejson",
  ],
};
