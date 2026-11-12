import { unified } from "@astrojs/markdown-remark";
import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";

import djlint from "../package.json" with { type: "json" };

// Pre-commit snippets pin the release the docs were built from.
function remarkDjlintVersion() {
  const walk = (node) => {
    if (typeof node.value === "string") {
      node.value = node.value.replaceAll("{{ djlint_version }}", djlint.version);
    }
    node.children?.forEach(walk);
  };
  return walk;
}

// Builds the djLint the demo runs, into public/static/py/. An ES module runs
// once per process, so a config reload in the dev server doesn't build it again.
const demoLock = {
  name: "demo-lock",
  hooks: {
    "astro:config:setup": async ({ command }) => {
      if (command === "build" || command === "dev") {
        await import("./demo-lock.mjs");
      }
    },
  },
};

export default defineConfig({
  site: "https://djlint.com",
  outDir: "_site",
  trailingSlash: "always",
  markdown: { processor: unified({ remarkPlugins: [remarkDjlintVersion] }) },
  integrations: [
    demoLock,
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
          attrs: { rel: "apple-touch-icon", href: "/static/img/apple-touch-icon.png" },
        },
      ],
      defaultLocale: "root",
      locales: {
        root: { label: "English", lang: "en" },
        zh: { label: "简体中文", lang: "zh-CN" },
        ja: { label: "日本語" },
        es: { label: "Español" },
        "pt-br": { label: "Português (Brasil)", lang: "pt-BR" },
        ru: { label: "Русский" },
        ko: { label: "한국어" },
        fr: { label: "Français" },
        de: { label: "Deutsch" },
        "zh-tw": { label: "繁體中文", lang: "zh-TW" },
        it: { label: "Italiano" },
        pl: { label: "Polski" },
        cs: { label: "Čeština" },
        tr: { label: "Türkçe" },
      },
      social: [
        { icon: "github", label: "GitHub", href: "https://github.com/djlint/djlint" },
        { icon: "discord", label: "Discord", href: "https://discord.gg/taghAqebzU" },
      ],
      editLink: { baseUrl: "https://github.com/djlint/djLint/edit/master/docs/" },
      lastUpdated: true,
      customCss: ["./src/styles/custom.css"],
      components: { Header: "./src/components/Header.astro", Hero: "./src/components/Hero.astro" },
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
            "zh-CN": "文档",
            ja: "ドキュメント",
            es: "Documentación",
            "pt-BR": "Documentação",
            ru: "Документация",
            ko: "문서",
            fr: "Documentation",
            de: "Dokumentation",
            "zh-TW": "說明文件",
            it: "Documentazione",
            pl: "Dokumentacja",
            cs: "Dokumentace",
            tr: "Belgeler",
          },
          items: [
            "docs/getting-started",
            "docs/formatter",
            "docs/linter",
            "docs/ignoring-code",
            "docs/configuration",
            "docs/integrations",
            "docs/python-api",
            "docs/best-practices",
            // English only: it shows the repository's CHANGELOG.md.
            {
              slug: "docs/changelog",
              label: "Changelog",
              translations: {
                "zh-CN": "更新日志",
                ja: "変更履歴",
                es: "Registro de cambios",
                "pt-BR": "Registro de alterações",
                ru: "История изменений",
                ko: "변경 내역",
                fr: "Journal des modifications",
                de: "Changelog",
                "zh-TW": "變更記錄",
                it: "Registro delle modifiche",
                pl: "Lista zmian",
                cs: "Seznam změn",
                tr: "Değişiklik günlüğü",
              },
            },
          ],
        },
        {
          label: "Template languages",
          translations: {
            "zh-CN": "模板语言",
            ja: "テンプレート言語",
            es: "Lenguajes de plantillas",
            "pt-BR": "Linguagens de template",
            ru: "Языки шаблонов",
            ko: "템플릿 언어",
            fr: "Langages de templates",
            de: "Template-Sprachen",
            "zh-TW": "範本語言",
            it: "Linguaggi di template",
            pl: "Języki szablonów",
            cs: "Šablonovací jazyky",
            tr: "Şablon dilleri",
          },
          items: [{ autogenerate: { directory: "docs/languages" } }],
        },
        "demo",
      ],
    }),
  ],
});
