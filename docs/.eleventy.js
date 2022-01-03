const Image = require("@11ty/eleventy-img");
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const criticalCss = require("eleventy-critical-css");
const slugify = require("slugify");
const metagen = require("eleventy-plugin-metagen");

const fs = require('fs');
const outdent = require('outdent');
const schema = require("@quasibit/eleventy-plugin-schema");


const slugifyCustom = (s) =>
  slugify(s, { lower: true, remove: /[*+~.()'"!:@]/g });

async function imageShortcode(src, alt, sizes, type='asdf', loading="lazy", decoding="async") {
  let metadata = await Image(src, {
    widths: [24, 300, 400, 500, 600, 800, 1200],
    formats: ["webp"],
    sharpWebpOptions: {
      options: {
        quality:70
      }
    },
    outputDir: "./_site/static/img/",
    urlPath: "/static/img/"
  });

  let imageAttributes = {
    alt,
    sizes,
    loading: loading,
    decoding: decoding,
  };

  if(type=="boxed"){
      return `<div class="block"><div class="box is-inlineblock">` + Image.generateHTML(metadata, imageAttributes) + `</div></div>`;
  }
  return Image.generateHTML(metadata, imageAttributes);
}

// from https://github.com/pusher/docs/blob/main/.eleventy.js
// widont is a function that takes a string and replaces the space between the last two words with a non breaking space. This stops typographic widows forming
const widont = (string) => {
  return string.split(" ").length > 2
    ? string.replace(/\s([^\s<]+)\s*$/, "\u00A0$1")
    : string;
};

module.exports = function(eleventyConfig) {

  eleventyConfig.setUseGitIgnore(false);
  eleventyConfig.addFilter("widont", widont);
  eleventyConfig.addWatchTarget("./src/static/");
  eleventyConfig.addNunjucksAsyncShortcode("image", imageShortcode);
  eleventyConfig.addTransform("htmlmin", require("./src/_utils/minify-html.js"));
  eleventyConfig.addPlugin(syntaxHighlight);
  eleventyConfig.addPlugin(metagen);
  eleventyConfig.addPlugin(criticalCss);

  eleventyConfig.addPlugin(schema);

  /* Markdown Plugins */
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
      symbol:"∞",
      placement: "before"
    }),
    slugify: slugifyCustom,
  };

  const mapping = {
    h1: 'title is-1',
    h2: 'title is-2',
    h3: 'title is-3',
    h4: 'title is-4',
    h5: 'title is-5',
    h6: 'title is-5',
    p: 'block',
    table: 'table'
  };

  markdownIt
      .use(markdownItAnchor, opts)
      .use(require("markdown-it-imsize"), { autofill: true })
      .use(require('@toycode/markdown-it-class'), mapping)
      .use(require('markdown-it-div'), 'div', {});

  eleventyConfig.setLibrary("md", markdownIt);

  // copy font
  eleventyConfig.addPassthroughCopy({
    "./node_modules/@fontsource/inter/files": "static/font/inter/files"
  });
  eleventyConfig.addPassthroughCopy({
    "./node_modules/@fontsource/rasa/files": "static/font/rasa/files"
  });

  // copy images
  eleventyConfig.addPassthroughCopy({
    "src/static/img": "static/img"
  });

  // copy robots
  eleventyConfig.addPassthroughCopy({
    "src/robots.txt": "robots.txt"
  });

  // copy favicon
  eleventyConfig.addPassthroughCopy({
    "src/static/img/favicon.ico": "favicon.ico"
  });

  eleventyConfig.addFilter("jsonify", (text) => {
    return JSON.stringify(text).replace(/(?:\\n\s*){2,}/g, "\\n");
  });

  eleventyConfig.addFilter("niceDate", (value) => {
    try{
      const options = {year: 'numeric', month: 'short', day: 'numeric' };
          return value.toLocaleDateString('en-us', options);
        } catch (e) {
          return value
        }

  });

  eleventyConfig.addFilter("algExcerpt", (text) => {
    return text
      .replace(/<code class="language-.*?">.*?<\/code>/gs, "")
      .replace(/<.*?>/g, "")
      .substring(0, 8000);
  });

  eleventyConfig.addCollection("algolia", function(collection) {
    return collection.getFilteredByGlob("**/*.md");
  });


  const icons = {
    note: '<span class="icon has-text-info"><i class="fas fa-pencil-alt"></i></span>',
    hint: "./src/_includes/icons/green_question.njk",
    alert: "./src/_includes/icons/red_triangle.njk"
  };

  eleventyConfig.addShortcode("admonition", function(icon, title, text) {
    return outdent`
    <article class="message ` + icon + ` box">
      <div class="message-header">
        <p>` + icons[icon] +title+`</p>
      </div>
      <div class="message-body">` + `${markdownIt.render(text)}`+ `</div>
    </article>`;
  });


  eleventyConfig.addFilter('markdown', value => {
    return `${markdownIt.render(value)}`;
  });

  const { fontawesomeSubset } = require('fontawesome-subset');
  fontawesomeSubset({
    brands:['discord', 'github'],
    regular:['envelope', 'life-ring'],
    solid: ['arrow-circle-right', 'pencil-alt', 'envelope', 'share', 'infinity', 'search', 'book', 'project-diagram', 'heart', 'address-card', 'server', 'database', 'ship', 'code', 'chart-bar', 'sitemap', 'tasks', 'lock', 'sliders-h', 'user', 'users', 'compass', 'download', 'sync-alt']
        }, '_site/static/font/fontawesome/webfonts');

  return {
    dir: {
      input: "src",
      formats: "njk",
      includes: "_includes",
      data: "_data",
      output: "_site"
    },
    templateFormats: ["md", "html", "njk", "11ty.js"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
    passthroughFileCopy: true
  };

};
