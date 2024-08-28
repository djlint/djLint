const generateContentHash = require("../lib/generate-content-hash.js");

const hash = generateContentHash("src/static/js/**/*.js");

module.exports = {
  scriptsJs: `/static/js/${hash}.js`,
};
