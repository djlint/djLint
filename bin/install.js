const { PythonShell } = require('python-shell');

PythonShell.defaultOptions = {};
const options = {
  mode: 'text',
  args: ['pip', 'install', 'djlint'],
  pythonOptions: ['-u'],
  env: { PYCHARM_HOSTED: 1 },
};

try {
  PythonShell.getVersionSync();

  PythonShell.run('-m', options, function (error, results) {
    if (error) throw error;
    console.log(results.join('\n'));
  });
} catch (e) {
  console.log(e.message);
  process.exit(1);
}
