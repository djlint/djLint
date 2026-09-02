const esmDefault = (module) => module.default ?? module;
const Image = esmDefault(require("@11ty/eleventy-img"));
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const slugify = require("slugify");
const metagen = require("eleventy-plugin-metagen");
const i18n = require("eleventy-plugin-i18n");
const translations = require("./src/_data/i18n");
const locales = require("./src/_data/locales");
const schema = require("@quasibit/eleventy-plugin-schema");
const editOnGithub = require("eleventy-plugin-edit-on-github");
const i18n_func = require("eleventy-plugin-i18n/i18n.js");
const rollupper = require("./src/_utils/rollupper");
const { nodeResolve } = require("@rollup/plugin-node-resolve");
const eleventySass = require("eleventy-sass");
const pluginRev = require("eleventy-plugin-rev");
const purgecss = require("@fullhuman/postcss-purgecss");
const postcss = require("postcss");

const slugifyCustom = (s) =>
  slugify(s, { lower: true, remove: /[*+~.()'"!:@]/g });

const schemaShortcodes = {};
const schemaReady = schema({
  addShortcode(name, callback) {
    schemaShortcodes[name] = callback;
  },
});

async function imageShortcode(
  src,
  alt,
  sizes,
  type = "asdf",
  loading = "lazy",
  decoding = "async",
) {
  let metadata = await Image(src, {
    widths: [24, 300, 400, 500, 600, 800, 1200],
    formats: ["webp", "png"],
    sharpWebpOptions: { options: { quality: 70 } },
    outputDir: "./_site/static/img/",
    urlPath: "/static/img/",
  });

  let imageAttributes = { alt, sizes, loading: loading, decoding: decoding };

  if (type == "boxed") {
    return (
      `<div class="block"><div class="box is-inlineblock">` +
      Image.generateHTML(metadata, imageAttributes) +
      `</div></div>`
    );
  }
  const largest = metadata.png[metadata.png.length - 1];
  return `<picture>
    ${Object.values(metadata)
      .map((imageFormat) => {
        return `  <source type="${
          imageFormat[0].sourceType
        }" srcset="${imageFormat
          .map((entry) => entry.srcset)
          .join(", ")}" sizes="${sizes}">`;
      })
      .join("\n")}
      <img
        src="${largest.url}"
        width="${largest.width}"
        height="${largest.height}"
        alt="${alt}"
        loading="lazy"
        decoding="async">
    </picture>`;
}

const joinLastTwoWords = (text) => {
  const words = text.split(" ");
  if (words.length < 3) return text;
  const last = words[words.length - 1].trimEnd();
  if (last === "" || last.includes("<")) return text;
  return `${words.slice(0, -1).join(" ")}\u00A0${last}`;
};

const emittedAtBuildTime = ["picture"];

const djlintTomlConfig = (value) =>
  value
    .replace(/\[tool\.djlint\.([^\]]+)\]/g, "[$1]")
    .replace(/\[tool\.djlint\]\n?/g, "")
    .trim();

module.exports = function (eleventyConfig) {
  eleventyConfig.addGlobalData(
    "djlint_version",
    require("../package.json").version,
  );
  eleventyConfig.setUseGitIgnore(false);
  eleventyConfig.addFilter("widont", joinLastTwoWords);
  eleventyConfig.addFilter("djlintTomlConfig", djlintTomlConfig);
  eleventyConfig.addWatchTarget("./src/static/");
  eleventyConfig.addNunjucksAsyncShortcode("image", imageShortcode);
  if (process.env.ELEVENTY_PRODUCTION == true) {
    eleventyConfig.addTransform(
      "htmlmin",
      require("./src/_utils/minify-html.js"),
    );
  }
  eleventyConfig.addPlugin(syntaxHighlight);
  eleventyConfig.addPlugin(metagen);
  eleventyConfig.addNunjucksAsyncShortcode(
    "jsonLdScript",
    async (meta, type, tags) => {
      await schemaReady;
      return schemaShortcodes.jsonLdScript(meta, type, tags);
    },
  );
  eleventyConfig.addNunjucksAsyncShortcode(
    "jsonLd",
    async (meta, type, tags) => {
      await schemaReady;
      return schemaShortcodes.jsonLd(meta, type, tags);
    },
  );
  eleventyConfig.addPlugin(rollupper, {
    rollup: {
      output: { format: "umd", dir: "_site/static/js" },
      plugins: [nodeResolve()],
    },
  });
  eleventyConfig.addPlugin(editOnGithub, {
    github_edit_repo: "https://github.com/djlint/djLint",
    github_edit_path: "/docs/",
    github_edit_branch: "master",
    github_edit_text: (page) => {
      i18n_options = Object.assign(
        {},
        { translations, fallbackLocales: { "*": "en-US" } },
      );

      return `<span class="icon-text"><span class="icon mr-1"><i class="fas fa-pencil"></i></span><span>${i18n_func(
        "edit_page",
        undefined,
        undefined,
        i18n_options,
        page,
      )}</span></span>`;
    },
    github_edit_class: "edit-on-github",
    github_edit_tag: "a",
    github_edit_attributes: 'target="_blank" rel="noopener"',
    github_edit_wrapper: undefined,
  });

  const markdownItAnchor = require("markdown-it-anchor");
  const markdownIt = require("markdown-it")({
    html: true,
    breaks: true,
    linkify: true,
    typographer: true,
  });

  const opts = {
    level: [2, 3, 4, 5],
    permalink: markdownItAnchor.permalink.linkInsideHeader({
      class: "link bn",
      symbol: "∞",
      placement: "before",
    }),
    slugify: slugifyCustom,
  };

  const mapping = {
    h1: "title is-1",
    h2: "title is-2",
    h3: "title is-3",
    h4: "title is-4",
    h5: "title is-5",
    h6: "title is-5",
    p: "block",
    table: "table",
  };

  markdownIt
    .use(markdownItAnchor, opts)
    .use(require("markdown-it-imsize"), { autofill: true })
    .use(require("@toycode/markdown-it-class"), mapping)
    .use(require("markdown-it-div"), "div", {});

  eleventyConfig.setLibrary("md", markdownIt);

  eleventyConfig.addPassthroughCopy({
    "./node_modules/@fontsource/inter/files": "static/font/inter/files",
  });
  eleventyConfig.addPassthroughCopy({
    "./node_modules/@fontsource/rasa/files": "static/font/rasa/files",
  });
  eleventyConfig.addPassthroughCopy({
    "./node_modules/@fontsource/crimson-pro/files":
      "static/font/crimson-pro/files",
  });

  eleventyConfig.addPassthroughCopy({ "src/static/img": "static/img" });

  eleventyConfig.addPassthroughCopy({ "src/robots.txt": "robots.txt" });

  eleventyConfig.addPassthroughCopy({
    "src/static/img/favicon.ico": "favicon.ico",
  });

  eleventyConfig.addPassthroughCopy({ "src/static/py": "static/py" });

  eleventyConfig.addPassthroughCopy({
    "src/static/js/worker.js": "static/js/worker.js",
  });

  eleventyConfig.addFilter("niceDate", (value) => {
    try {
      const options = { year: "numeric", month: "short", day: "numeric" };
      return value.toLocaleDateString("en-us", options);
    } catch (e) {
      return value;
    }
  });

  eleventyConfig.addFilter("year", (value) => {
    try {
      const options = { year: "numeric" };
      return value.toLocaleDateString("en-us", options);
    } catch (e) {
      return value;
    }
  });

  const icons = {
    note: '<span class="icon has-text-info mr-1"><i class="fas fa-pencil"></i></span>',
  };

  eleventyConfig.addShortcode("admonition", function (icon, title, text) {
    return `<article class="message ${icon} box">
  <div class="message-header">
    <p>${icons[icon]} ${title}</p>
  </div>
  <div class="message-body">${markdownIt.render(text)}</div>
</article>`;
  });

  eleventyConfig.addFilter("markdown", (value) => {
    return `${markdownIt.render(value)}`;
  });

  eleventyConfig.addPlugin(pluginRev);

  eleventyConfig.addPlugin(eleventySass, [
    {
      rev: true,
      postcss: postcss([
        esmDefault(require("postcss-nested")),
        purgecss({
          content: ["./src/**/*.njk", "./src/**/*.md", "./src/**/*.js"],
          safelist: {
            standard: emittedAtBuildTime,
            deep: [
              /token/,
              /headShake/,
              /zoomIn/,
              /fadeInUp/,
              /pre/,
              /code/,
              /block/,
              /box/,
              /title/,
              /is-\d/,
              /table/,
              /message/,
              /message-header/,
              /message-body/,
              /panel-block/,
              /p-3/,
              /my-3/,
              /is-block/,
              /is-justify-content-space-between/,
              /is-light/,
              /is-active/,
              /is-info/,
              /is-link/,
              /fa-*/,
              /mr-1/,
              /mr-2/,
              /has-text-info/,
              /option/,
              /is-rounded/,
            ],
          },
        }),
        require("autoprefixer"),
        require("cssnano"),
      ]),
    },
  ]);

  const { fontawesomeSubset } = require("fontawesome-subset");
  fontawesomeSubset(
    {
      brands: ["discord", "github"],
      regular: ["envelope"],
      solid: [
        "globe",
        "circle-arrow-right",
        "pencil",
        "infinity",
        "download",
        "code-commit",
        "spinner",
        "circle-question",
      ],
    },
    "_site/static/font/fontawesome/webfonts",
  );

  eleventyConfig.addPlugin(i18n, {
    translations,
    fallbackLocales: { "*": "en-US" },
  });

  eleventyConfig.addFilter("baseUrl", (text) => {
    return text.replace(/(?:ru)\//g, "");
  });

  eleventyConfig.addFilter("i18n_locale", (current_locale, locale_list) => {
    return locale_list.filter((x) => {
      return x.code === (current_locale ?? "en-US");
    })[0].label;
  });

  eleventyConfig.addFilter("i18n_urls", (page, all) => {
    var locale_urls = locales
      .map((x) => {
        if (x.url != "") return x.url;
      })
      .filter((x) => {
        return x !== undefined;
      });

    var split_url = page.split("/").length > 1 ? page.split("/")[1] : "";

    var active_local = "";

    locale_urls.forEach((locale) => {
      if (locale === split_url) {
        active_local = locale;
        return true;
      }
      return false;
    });

    var remaining_locals = locales
      .map((x) => {
        return x.url;
      })
      .filter((x) => {
        return x !== active_local;
      });

    var i18n_pages = [];

    var valid_urls = all.map((x) => {
      return x.url;
    });

    remaining_locals.forEach((x) => {
      var new_url = ("/" + page.replace(active_local, x)).replace(
        /\/{2,}/,
        "/",
      );
      if (valid_urls.indexOf(new_url) !== -1) {
        i18n_pages.push({
          url: new_url,
          meta: locales.filter((y) => {
            return y.url === x;
          })[0],
        });
      }
    });

    return i18n_pages;
  });

  return {
    dir: {
      input: "src",
      formats: "njk",
      includes: "_includes",
      data: "_data",
      output: "_site",
    },
    templateFormats: ["md", "html", "njk", "11ty.js"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
    passthroughFileCopy: true,
  };
};
