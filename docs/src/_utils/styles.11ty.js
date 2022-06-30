const util = require('util');
const sass = require('sass'); // `npm i -D sass`
const renderSass = util.promisify(sass.render);
const purgecss = require('@fullhuman/postcss-purgecss');
const postcss = require('postcss');
const generateContentHash = require('../lib/generateContentHash');

module.exports = class {
  async data() {
    return {
      permalink: `/static/css/${generateContentHash(
        'src/static/**/*.{scss,css}',
      )}.css`,
      eleventyExcludeFromCollections: true,
    };
  }

  async render() {
    const result = await renderSass({
      file: 'src/static/css/site.scss',
    });

    return await postcss([
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
            /is-block/,
            /is-justify-content-space-between/,
            /is-light/,
            /is-active/,
            /is-info/,
            /fa-*/,
            /mr-1/,
            /mr-2/,
            /has-text-info/,
          ],
        },
      }),
      require('autoprefixer'),
      require('cssnano'),
    ])
      .process(result.css, { from: undefined })
      .then((result) => result.css);
  }
};
