import { unified } from "@astrojs/markdown-remark";
import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";
import djlint from "../package.json" with { type: "json" };

// Pre-commit snippets pin the release the docs were built from.
function remarkDjlintVersion() {
  const walk = (node) => {
    if (typeof node.value === "string") {
      node.value = node.value.replaceAll(
        "{{ djlint_version }}",
        djlint.version,
      );
    }
    node.children?.forEach(walk);
  };
  return walk;
}

export default defineConfig({
  site: "https://djlint.com",
  outDir: "_site",
  trailingSlash: "always",
  markdown: { processor: unified({ remarkPlugins: [remarkDjlintVersion] }) },
  integrations: [
    starlight({
      title: "djLint",
      logo: {
        light: "./src/assets/logo-wide-light.svg",
        dark: "./src/assets/logo-wide-dark.svg",
        replacesTitle: true,
      },
      favicon: "/static/img/logo.svg",
      head: [
        {
          tag: "link",
          attrs: {
            rel: "apple-touch-icon",
            href: "/static/img/apple-touch-icon.png",
          },
        },
      ],
      defaultLocale: "root",
      locales: {
        root: { label: "English", lang: "en" },
        ru: { label: "Русский" },
        fr: { label: "Français" },
        zh: { label: "简体中文", lang: "zh-CN" },
      },
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/djlint/djlint",
        },
        {
          icon: "discord",
          label: "Discord",
          href: "https://discord.gg/taghAqebzU",
        },
      ],
      editLink: {
        baseUrl: "https://github.com/djlint/djLint/edit/master/docs/",
      },
      lastUpdated: true,
      customCss: ["./src/styles/custom.css"],
      components: {
        Header: "./src/components/Header.astro",
        Hero: "./src/components/Hero.astro",
      },
      expressiveCode: {
        themes: ["tokyo-night", "github-light"],
        styleOverrides: {
          borderRadius: "0.5rem",
          codeFontFamily: "var(--sl-font-mono)",
          uiFontFamily: "var(--sl-font)",
          frames: { shadowColor: "transparent" },
        },
      },
      sidebar: [
        {
          label: "Documentation",
          translations: {
            ru: "Документация",
            fr: "Documentation",
            "zh-CN": "文档",
          },
          items: [
            "docs/getting-started",
            "docs/formatter",
            "docs/linter",
            "docs/ignoring-code",
            "docs/configuration",
            "docs/integrations",
            "docs/best-practices",
            // English only: it shows the repository's CHANGELOG.md.
            {
              slug: "docs/changelog",
              label: "Changelog",
              translations: {
                ru: "Изменения",
                fr: "Changelog",
                "zh-CN": "更新日志",
              },
            },
          ],
        },
        {
          label: "Template languages",
          translations: {
            ru: "Языки шаблонов",
            fr: "Langages de modèles",
            "zh-CN": "模板语言",
          },
          items: [{ autogenerate: { directory: "docs/languages" } }],
        },
        "demo",
      ],
    }),
  ],
});
