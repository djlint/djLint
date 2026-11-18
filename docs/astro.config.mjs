import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { unified } from "@astrojs/markdown-remark";
import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";
import slugify from "slugify";
import starlightLlmsTxt from "starlight-llms-txt";

import djlint from "../package.json" with { type: "json" };

/** @import { AstroIntegration } from "astro" */
/** @import { Nodes as HastNodes, Root as HastRoot } from "hast" */
/** @import { Heading, Nodes as MdastNodes, Root as MdastRoot } from "mdast" */
/** @import { VFile } from "vfile" */

/**
 * @param {(node: MdastNodes) => void} visit
 * @returns {(tree: MdastRoot) => void} A plugin that calls visit on every node of the tree.
 */
function visitMdast(visit) {
  /** @param {MdastNodes} node */
  function walk(node) {
    visit(node);
    if ("children" in node) {
      for (const child of node.children) {
        walk(child);
      }
    }
  }
  return walk;
}

// Pre-commit snippets pin the release the docs were built from.
function remarkDjlintVersion() {
  return visitMdast((node) => {
    if ("value" in node) {
      node.value = node.value.replaceAll("{{ djlint_version }}", djlint.version);
    }
  });
}

// The examples are templates, not plain HTML. Twig's grammar is HTML plus the
// {{ }}, {% %} and {# #} tags that Django, Jinja and Nunjucks share, so code
// marked html is highlighted with it and its template syntax isn't left grey.
function remarkTemplateCode() {
  return visitMdast((node) => {
    if (node.type === "code" && node.lang === "html") {
      node.lang = "twig";
    }
  });
}

// Heading ids as the Eleventy site made them, transliterated to ASCII, so links
// to sections of the translated pages keep working. CHANGELOG.md lives outside
// src/content/docs/ and gets its ids from remarkChangelog.
/**
 * @param {string} text
 * @returns {string} The id the Eleventy site gave a heading with this text.
 */
function eleventySlug(text) {
  return slugify(text, { lower: true, remove: /[*+~.()'"!:@]/gu });
}

/**
 * @param {HastNodes} node
 * @returns {string} The text in the node.
 */
function hastText(node) {
  if (node.type === "text") {
    return node.value;
  }
  return "children" in node ? node.children.map((child) => hastText(child)).join("") : "";
}

/**
 * @param {HastRoot} tree
 * @param {VFile} file
 */
function addEleventyHeadingIds(tree, file) {
  if (!/[\\/]src[\\/]content[\\/]docs[\\/]/u.test(file.path)) {
    return;
  }
  const used = new Set();
  /** @param {HastNodes} node */
  function walk(node) {
    if (node.type === "element" && /^h[2-5]$/u.test(node.tagName) && !("id" in node.properties)) {
      const slug = eleventySlug(hastText(node));
      let id = slug;
      for (let i = 1; used.has(id); i += 1) {
        id = `${slug}-${i}`;
      }
      used.add(id);
      Object.assign(node.properties, { id });
    }
    if ("children" in node) {
      for (const child of node.children) {
        walk(child);
      }
    }
  }
  walk(tree);
}

function rehypeEleventyHeadingIds() {
  return addEleventyHeadingIds;
}

/**
 * @param {MdastNodes | undefined} node
 * @returns {node is Heading} Whether the node starts a section of the changelog.
 */
function isChangelogSection(node) {
  return node?.type === "heading" && node.depth === 2;
}

/**
 * @param {MdastRoot} tree
 * @param {VFile} file
 */
function trimChangelog(tree, file) {
  if (!/[\\/]CHANGELOG\.md$/u.test(file.path)) {
    return;
  }
  const nodes = tree.children.slice(tree.children.findIndex((node) => isChangelogSection(node)));
  tree.children = nodes.filter((node, i) => {
    if (!isChangelogSection(node)) {
      return true;
    }
    const [title] = node.children;
    // Text, or inline code or HTML, if a heading ever starts with that.
    const version = title && "value" in title ? /^\[(.+?)\]/u.exec(title.value)?.[1] : null;
    if (version === "Unreleased" && (nodes[i + 1] == null || isChangelogSection(nodes[i + 1]))) {
      return false;
    }
    if (version != null) {
      node.data = { hProperties: { id: eleventySlug(version) } };
    }
    return true;
  });
}

// The changelog page starts CHANGELOG.md at its first "##": the "# Changelog"
// above it would repeat the page title, and the intro is only a link to
// Semantic Versioning. An empty Unreleased section goes too. A release heading
// ("[1.50.4] - 2026-11-15") gets the id the old site gave it, the version
// without dots ("1504"), so old links to a release still land on it.
function remarkChangelog() {
  return trimChangelog;
}

// Builds the djLint the demo runs, into public/static/py/, in a process of its
// own: Pyodide stays out of Astro's memory. The flag on globalThis outlives a
// config reload in the dev server, so a reload doesn't build it again.
const flags = /** @type {typeof globalThis & { djlintDemoLockBuilt?: boolean }} */ (globalThis);
/** @type {AstroIntegration} */
const demoLock = {
  name: "demo-lock",
  hooks: {
    "astro:config:setup": ({ command }) => {
      if ((command === "build" || command === "dev") && flags.djlintDemoLockBuilt !== true) {
        execFileSync(process.execPath, [fileURLToPath(new URL("demo-lock.mjs", import.meta.url))], {
          stdio: "inherit",
        });
        flags.djlintDemoLockBuilt = true;
      }
    },
  },
};

// Every page gets a CSP <meta> right after its charset that runs no inline
// script but the page's own, by hash. Astro's security.csp would leave out
// Starlight's is:inline scripts, so the hashes come from the built HTML.
// Vite inlines the smallest font files as data: URLs, the stylesheets draw
// icons from data: URLs, the home page shows a shields.io badge, and Pagefind
// fetches its index in the page when its worker fails. Styles stay unrestricted inline: Expressive Code
// colors code with style attributes, and CodeMirror writes its styles into a
// <style> at run time. frame-ancestors can't go in a <meta>: public/_headers
// sends it.
const CSP = [
  "default-src 'none'",
  "connect-src 'self'",
  "font-src 'self' data:",
  "img-src 'self' data: https://img.shields.io",
  "style-src 'self' 'unsafe-inline'",
  "base-uri 'none'",
  "form-action 'none'",
].join("; ");

/**
 * @param {string} html
 * @returns {string} The CSP sources of the inline scripts in the page.
 */
function scriptHashes(html) {
  const hashes = new Set();
  for (const [, attrs = "", body] of html.matchAll(/<script(\s[^>]*)?>([\s\S]*?)<\/script>/gu)) {
    if (body && !/\ssrc=/u.test(attrs)) {
      hashes.add(`'sha256-${createHash("sha256").update(body).digest("base64")}'`);
    }
  }
  return [...hashes].join(" ");
}

/** @type {AstroIntegration} */
const csp = {
  name: "csp",
  hooks: {
    "astro:build:done": ({ dir }) => {
      const root = fileURLToPath(dir);
      const charset = '<meta charset="utf-8"/>';
      for (const file of readdirSync(root, { encoding: "utf8", recursive: true })) {
        if (!file.endsWith(".html")) {
          continue;
        }
        const htmlPath = path.join(root, file);
        const html = readFileSync(htmlPath, "utf8");
        if (!html.includes(charset)) {
          throw new Error(`${file} has no ${charset} to put the CSP after`);
        }
        const policy = `${CSP}; script-src 'self' ${scriptHashes(html)}`;
        const meta = `<meta http-equiv="content-security-policy" content="${policy}"/>`;
        writeFileSync(htmlPath, html.replace(charset, charset + meta));
      }
    },
  },
};

export default defineConfig({
  site: "https://djlint.com",
  trailingSlash: "always",
  markdown: {
    processor: unified({
      remarkPlugins: [remarkDjlintVersion, remarkTemplateCode, remarkChangelog],
      rehypePlugins: [rehypeEleventyHeadingIds],
    }),
  },
  integrations: [
    demoLock,
    csp,
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
      customCss: ["./src/styles/custom.css"],
      components: {
        Footer: "./src/components/Footer.astro",
        Header: "./src/components/Header.astro",
        Hero: "./src/components/Hero.astro",
      },
      // Starlight's heading anchor links for CHANGELOG.md too, which lives in
      // the repository root.
      markdown: { processedDirs: [".."] },
      routeMiddleware: "./src/route-data.ts",
      // llms.txt and its full and small versions, for AI assistants, from the
      // English docs. The demo and the changelog say nothing they need: they
      // render nothing there, as the home page does (see Home.astro), and
      // `exclude` drops them from llms-small.txt, the only file it applies to.
      plugins: [
        starlightLlmsTxt({
          description:
            "djLint is a linter and formatter for HTML templates: Django, Jinja, Twig, Nunjucks, Handlebars, Mustache, Liquid, Go templates, Angular, Tera, Askama and Mako.",
          exclude: ["demo", "docs/changelog"],
        }),
      ],
      expressiveCode: {
        themes: ["tokyo-night", "github-light"],
        // Both themes paint code on the page's own background, so the blocks
        // take their colors from custom.css, which tints them apart from it.
        styleOverrides: {
          borderRadius: "0.5rem",
          borderColor: "var(--dj-block-line)",
          codeBackground: "var(--dj-block-bg)",
          codeFontFamily: "var(--sl-font-mono)",
          uiFontFamily: "var(--sl-font)",
          frames: {
            editorActiveTabBackground: "var(--dj-block-bg)",
            editorTabBarBackground: "var(--dj-block-bar)",
            shadowColor: "transparent",
            terminalBackground: "var(--dj-block-bg)",
            terminalTitlebarBackground: "var(--dj-block-bar)",
          },
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
