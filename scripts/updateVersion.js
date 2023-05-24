const fs = require('fs/promises');
const prettier = require('prettier');

const updateVersion = async () => {
  const nextVersion = process.argv[2];
  const packageJson = JSON.parse(
    (await fs.readFile('package.json')).toString(),
  );
  packageJson.scripts.postinstall = `python3 -m pip install djlint==${nextVersion}`;
  await fs.writeFile(
    'package.json',
    prettier.format(JSON.stringify(packageJson), { filepath: 'package.json' }),
  );
};

updateVersion();
