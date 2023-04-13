const Image = require('@11ty/eleventy-img');
const syntaxHighlight = require('@11ty/eleventy-plugin-syntaxhighlight');
const slugify = require('slugify');
const metagen = require('eleventy-plugin-metagen');
const i18n = require('eleventy-plugin-i18n');
const translations = require('./src/_data/i18n');
const locales = require('./src/_data/locales');
const fs = require('fs');
const outdent = require('outdent');
const schema = require('@quasibit/eleventy-plugin-schema');
const editOnGithub = require('eleventy-plugin-edit-on-github');
const i18n_func = require('eleventy-plugin-i18n/i18n.js');
const rollupper = require('./src/_utils/rollupper');
const { nodeResolve } = require('@rollup/plugin-node-resolve');
const eleventySass = require('eleventy-sass');
const pluginRev = require('eleventy-plugin-rev');
const purgecss = require('@fullhuman/postcss-purgecss');
const postcss = require('postcss');

const slugifyCustom = (s) =>
  slugify(s, { lower: true, remove: /[*+~.()'"!:@]/g });

async function imageShortcode(
  src,
  alt,
  sizes,
  type = 'asdf',
  loading = 'lazy',
  decoding = 'async',
) {
  let metadata = await Image(src, {
    widths: [24, 300, 400, 500, 600, 800, 1200],
    formats: ['webp', 'png'],
    sharpWebpOptions: {
      options: {
        quality: 70,
      },
    },
    outputDir: './_site/static/img/',
    urlPath: '/static/img/',
  });

  let imageAttributes = {
    alt,
    sizes,
    loading: loading,
    decoding: decoding,
  };

  if (type == 'boxed') {
    return (
      `<div class="block"><div class="box is-inlineblock">` +
      Image.generateHTML(metadata, imageAttributes) +
      `</div></div>`
    );
  }
  // using custom code so that we can return the highest src in img as old browsers don't auto upscale.
  let lowsrc = metadata.png[0];
  let highsrc = metadata.png[metadata.png.length - 1];
  return `<picture>
    ${Object.values(metadata)
      .map((imageFormat) => {
        return `  <source type="${
          imageFormat[0].sourceType
        }" srcset="${imageFormat
          .map((entry) => entry.srcset)
          .join(', ')}" sizes="${sizes}">`;
      })
      .join('\n')}
      <img
        src="${highsrc.url}"
        width="${highsrc.width}"
        height="${highsrc.height}"
        alt="${alt}"
        loading="lazy"
        decoding="async">
    </picture>`;
}

// from https://github.com/pusher/docs/blob/main/.eleventy.js
// widont is a function that takes a string and replaces the space between the last two words with a non breaking space. This stops typographic widows forming
const widont = (string) => {
  return string.split(' ').length > 2
    ? string.replace(/\s([^\s<]+)\s*$/, '\u00A0$1')
    : string;
};

module.exports = function (eleventyConfig) {
  eleventyConfig.addGlobalData(
    'djlint_version',
    require('../package.json').version,
  );
  eleventyConfig.setUseGitIgnore(false);
  eleventyConfig.addFilter('widont', widont);
  eleventyConfig.addWatchTarget('./src/static/');
  eleventyConfig.addNunjucksAsyncShortcode('image', imageShortcode);
  if (process.env.ELEVENTY_PRODUCTION == true) {
    eleventyConfig.addTransform(
      'htmlmin',
      require('./src/_utils/minify-html.js'),
    );
  }
  eleventyConfig.addPlugin(syntaxHighlight);
  eleventyConfig.addPlugin(metagen);
  eleventyConfig.addPlugin(schema);
  eleventyConfig.addPlugin(rollupper, {
    rollup: {
      output: {
        format: 'umd',
        dir: '_site/static/js',
      },
      plugins: [nodeResolve()],
    },
  });
  eleventyConfig.addPlugin(editOnGithub, {
    // required
    github_edit_repo: 'https://github.com/Riverside-Healthcare/djLint',
    // optional: defaults
    github_edit_path: '/docs/', // non-root location in git url. root is assumed
    github_edit_branch: 'master',
    github_edit_text: (page) => {
      i18n_options = Object.assign(
        {},
        {
          translations,
          fallbackLocales: {
            '*': 'en-US',
          },
        },
      );

      return `<span class="icon-text"><span class="icon mr-1"><i class="fas fa-pencil"></i></span><span>${i18n_func(
        'edit_page',
        undefined,
        undefined,
        i18n_options,
        page,
      )}</span></span>`;
      return x.inputPath;
    },
    github_edit_class: 'edit-on-github',
    github_edit_tag: 'a',
    github_edit_attributes: 'target="_blank" rel="noopener"',
    github_edit_wrapper: undefined, //ex: "<div stuff>${edit_on_github}</div>"
  });

  /* Markdown Plugins */
  const markdownItAnchor = require('markdown-it-anchor');
  const markdownIt = require('markdown-it')({
    html: true,
    breaks: true,
    linkify: true,
    typographer: true,
  });

  const opts = {
    level: [2, 3, 4, 5],
    permalink: markdownItAnchor.permalink.linkInsideHeader({
      class: 'link bn',
      symbol: '∞',
      placement: 'before',
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
    table: 'table',
  };

  markdownIt
    .use(markdownItAnchor, opts)
    .use(require('markdown-it-imsize'), { autofill: true })
    .use(require('@toycode/markdown-it-class'), mapping)
    .use(require('markdown-it-div'), 'div', {});

  eleventyConfig.setLibrary('md', markdownIt);

  // copy font
  eleventyConfig.addPassthroughCopy({
    './node_modules/@fontsource/inter/files': 'static/font/inter/files',
  });
  eleventyConfig.addPassthroughCopy({
    './node_modules/@fontsource/rasa/files': 'static/font/rasa/files',
  });
  eleventyConfig.addPassthroughCopy({
    './node_modules/@fontsource/crimson-pro/files':
      'static/font/crimson-pro/files',
  });

  // copy images
  eleventyConfig.addPassthroughCopy({
    'src/static/img': 'static/img',
  });

  // copy robots
  eleventyConfig.addPassthroughCopy({
    'src/robots.txt': 'robots.txt',
  });

  // copy favicon
  eleventyConfig.addPassthroughCopy({
    'src/static/img/favicon.ico': 'favicon.ico',
  });

  // copy wheels
  eleventyConfig.addPassthroughCopy({
    'src/static/py': 'static/py',
  });

  // copy python
  eleventyConfig.addPassthroughCopy({
    'src/static/js/worker.js': 'static/js/worker.js',
  });

  eleventyConfig.addFilter('jsonify', (text) => {
    return JSON.stringify(text).replace(/(?:\\n\s*){2,}/g, '\\n');
  });

  eleventyConfig.addFilter('niceDate', (value) => {
    try {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return value.toLocaleDateString('en-us', options);
    } catch (e) {
      return value;
    }
  });

  eleventyConfig.addFilter('year', (value) => {
    try {
      const options = { year: 'numeric' };
      return value.toLocaleDateString('en-us', options);
    } catch (e) {
      return value;
    }
  });

  eleventyConfig.addFilter('algExcerpt', (text) => {
    return text
      .replace(/<code class="language-.*?">.*?<\/code>/gs, '')
      .replace(/<.*?>/g, '')
      .substring(0, 8000);
  });

  eleventyConfig.addCollection('algolia', function (collection) {
    return collection.getFilteredByGlob('**/*.md');
  });

  const icons = {
    note: '<span class="icon has-text-info mr-1"><i class="fas fa-pencil"></i></span>',
  };

  eleventyConfig.addShortcode('admonition', function (icon, title, text) {
    return outdent`
    <article class="message ${icon} box">
      <div class="message-header">
        <p>${icons[icon]} ${title}</p>
      </div>
      <div class="message-body">${markdownIt.render(text)}</div>
    </article>`;
  });

  eleventyConfig.addFilter('markdown', (value) => {
    return `${markdownIt.render(value)}`;
  });

  eleventyConfig.addPlugin(pluginRev);

  eleventyConfig.addPlugin(eleventySass, [
    {
      rev: true,
      postcss: postcss([
        require('postcss-nested'),
        purgecss({
          content: ['./src/**/*.njk', './src/**/*.md', './src/**/*.js'],
          safelist: {
            deep: [
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
              /has-background-white-ter/,
              /is-rounded/,
            ],
          },
        }),
        require('autoprefixer'),
        require('cssnano'),
      ]),
    },
  ]);

  const { fontawesomeSubset } = require('fontawesome-subset');
  fontawesomeSubset(
    {
      brands: ['discord', 'github'],
      regular: ['envelope'],
      solid: [
        'globe',
        'circle-arrow-right',
        'pencil',
        'infinity',
        'download',
        'code-commit',
        'spinner',
        'circle-question',
      ],
    },
    '_site/static/font/fontawesome/webfonts',
  );

  eleventyConfig.addPlugin(i18n, {
    translations,
    fallbackLocales: {
      '*': 'en-US',
    },
  });

  eleventyConfig.addFilter('baseUrl', (text) => {
    return text.replace(/(?:ru)\//g, '');
  });

  eleventyConfig.addFilter('i18n_locale', (current_locale, locale_list) => {
    return locale_list.filter((x) => {
      return x.code === (current_locale ?? 'en-US');
    })[0].label;
  });

  eleventyConfig.addFilter('i18n_urls', (page, all) => {
    var locale_urls = locales
      .map((x) => {
        if (x.url != '') return x.url;
      })
      .filter((x) => {
        return x !== undefined;
      });

    var split_url = page.split('/').length > 1 ? page.split('/')[1] : '';

    // find the current locale
    var active_local = '';

    locale_urls.forEach((locale) => {
      if (locale === split_url) {
        active_local = locale;
        return true;
      }
      return false;
    });

    // get remaining locales
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
      var new_url = ('/' + page.replace(active_local, x)).replace(
        /\/{2,}/,
        '/',
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
      input: 'src',
      formats: 'njk',
      includes: '_includes',
      data: '_data',
      output: '_site',
    },
    templateFormats: ['md', 'html', 'njk', '11ty.js'],
    htmlTemplateEngine: 'njk',
    markdownTemplateEngine: 'njk',
    passthroughFileCopy: true,
  };
};
