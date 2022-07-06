const generateContentHash = require('../lib/generate-content-hash.js');

const hash = generateContentHash('src/static/**/*.{scss,css}');

module.exports = {
  stylesCss: `/static/css/${hash}.css`,
};
