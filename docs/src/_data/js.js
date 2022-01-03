const path = require('path');
const generateContentHash = require('../lib/generateContentHash');

const hash = generateContentHash('src/static/js/**/*.js');

module.exports = {
  scriptsJs: `/static/js/${hash}.js`,
};
