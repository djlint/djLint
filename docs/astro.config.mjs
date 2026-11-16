import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { unified } from "@astrojs/markdown-remark";
import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";
import slugify from "slugify";
import starlightLlmsTxt from "starlight-llms-txt";

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

// Heading ids as the Eleventy site made them, transliterated to ASCII, so links
// to sections of the translated pages keep working. Astro's own ids (GitHub's)
// stay on the changelog, whose CHANGELOG.md lives outside src/content/docs/.
function rehypeEleventyHeadingIds() {
  const text = (node) =>
    node.type === "text" ? node.value : (node.children?.map(text).join("") ?? "");
  const walk = (node, visit) => {
    visit(node);
    node.children?.forEach((child) => walk(child, visit));
  };
  return (tree, file) => {
    if (!/[\\/]src[\\/]content[\\/]docs[\\/]/u.test(file.path ?? "")) {
      return;
    }
    const used = new Set();
    walk(tree, (node) => {
      if (!/^h[2-5]$/u.test(node.tagName ?? "") || node.properties?.id) {
        return;
      }
      const slug = slugify(text(node), { lower: true, remove: /[*+~.()'"!:@]/g });
      let id = slug;
      for (let i = 1; used.has(id); i++) {
        id = `${slug}-${i}`;
      }
      used.add(id);
      node.properties.id = id;
    });
  };
}

// Builds the djLint the demo runs, into public/static/py/, in a process of its
// own: Pyodide stays out of Astro's memory. The flag on globalThis outlives a
// config reload in the dev server, so a reload doesn't build it again.
const demoLock = {
  name: "demo-lock",
  hooks: {
    "astro:config:setup": ({ command }) => {
      if ((command === "build" || command === "dev") && !globalThis.djlintDemoLockBuilt) {
        execFileSync(process.execPath, [fileURLToPath(new URL("demo-lock.mjs", import.meta.url))], {
          stdio: "inherit",
        });
        globalThis.djlintDemoLockBuilt = true;
      }
    },
  },
};

export default defineConfig({
  site: "https://djlint.com",
  trailingSlash: "always",
  markdown: {
    processor: unified({
      remarkPlugins: [remarkDjlintVersion],
      rehypePlugins: [rehypeEleventyHeadingIds],
    }),
  },
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
        // The picture a link preview shows in chats and social networks.
        {
          tag: "meta",
          attrs: { property: "og:image", content: "https://djlint.com/static/img/icon.png" },
        },
        { tag: "meta", attrs: { property: "og:image:alt", content: "djLint" } },
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
        { icon: "seti:python", label: "PyPI", href: "https://pypi.org/project/djlint/" },
      ],
      editLink: { baseUrl: "https://github.com/djlint/djLint/edit/master/docs/" },
      lastUpdated: true,
      customCss: ["./src/styles/custom.css"],
      components: { Header: "./src/components/Header.astro", Hero: "./src/components/Hero.astro" },
      routeMiddleware: "./src/route-data.ts",
      // llms.txt and its full and small versions, for AI assistants, from the
      // English docs. The demo and the changelog say nothing they need, and
      // the home page renders nothing there (see Home.astro).
      plugins: [
        starlightLlmsTxt({
          description:
            "djLint is a linter and formatter for HTML templates: Django, Jinja, Twig, Nunjucks, Handlebars, Mustache, Liquid, Go templates, Angular, Tera, Askama and Mako.",
          exclude: ["demo", "docs/changelog"],
        }),
      ],
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
