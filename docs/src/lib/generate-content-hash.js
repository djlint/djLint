const fs = require('fs');
const glob = require('fast-glob');
const md5 = require('md5');

function generateContentHash(dir) {
  const sourceFiles = glob.sync([`${dir}`]);
  const sourceContent = sourceFiles
    .map((sourceFile) => fs.readFileSync(sourceFile))
    .join('');
  return md5(sourceContent).slice(0, 8);
}

module.exports = generateContentHash;
