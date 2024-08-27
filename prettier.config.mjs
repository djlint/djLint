/**
 * @type {import('prettier').Config & import("@ianvs/prettier-plugin-sort-imports").PluginConfig}
 */
export default {
  singleQuote: true,
  plugins: [
    '@ianvs/prettier-plugin-sort-imports',
    'prettier-plugin-packagejson',
  ],
};
