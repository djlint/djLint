const path = require('path');
const generateContentHash = require('../lib/generateContentHash');

const hash = generateContentHash('src/static/**/*.{scss,css}');

module.exports = {
  stylesCss: `/static/css/${hash}.css`,
};
