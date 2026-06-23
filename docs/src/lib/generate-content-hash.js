const fs = require('fs');
const glob = require('fast-glob');
const crypto = require('node:crypto');

function generateContentHash(dir) {
  const sourceFiles = glob.sync([`${dir}`]);
  const sourceContent = sourceFiles
    .map((sourceFile) => fs.readFileSync(sourceFile))
    .join('');
  return crypto
    .createHash('md5')
    .update(sourceContent)
    .digest('hex')
    .slice(0, 8);
}

module.exports = generateContentHash;
