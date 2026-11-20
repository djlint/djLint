import { createRequire } from "node:module";

/*
 * Stylelint resolves `extends` like ESM imports, which ignore NODE_PATH, so the
 * configs installed in the pre-commit hook environment are resolved here.
 */
const require = createRequire(import.meta.url);

/** @type {import('stylelint').Config} */
const config = {
  extends: [
    require.resolve("stylelint-config-standard"),
    require.resolve("stylelint-config-recess-order"),
  ],
  overrides: [
    {
      // The <style> of the Astro components, and :global(), Astro's way to style
      // what a component doesn't render itself.
      customSyntax: require.resolve("postcss-html"),
      files: ["**/*.astro"],
      rules: { "selector-pseudo-class-no-unknown": [true, { ignorePseudoClasses: ["global"] }] },
    },
  ],
  // Declares the --dj-* custom properties, so the rules check what var() gives in the components.
  referenceFiles: "src/styles/custom.css",
  reportDescriptionlessDisables: true,
  reportInvalidScopeDisables: true,
  reportNeedlessDisables: true,
  reportUnscopedDisables: true,
  rules: {
    "color-no-invalid-hex": true,
    "function-linear-gradient-no-nonstandard-direction": true,
    "function-no-unknown": true,
    "function-url-no-scheme-relative": true,
    "no-unknown-animations": true,
    "no-unknown-custom-media": true,
    "unit-no-unknown": true,
  },
};

export default config;
