const process = require('process');
const { PythonShell } = require('python-shell');

PythonShell.defaultOptions = {
  mode: 'text',
  pythonOptions: ['-u'],
  env: { PYCHARM_HOSTED: 1 }, // Force color
};

function clean(output) {
  if (typeof output === 'string' || output instanceof String)
  {
    return output.replaceAll('python -m ', '');
  }
  return output;
}

const yargs = require('yargs');

const stdin = process.stdin;

function getStdin() {
  // https://github.com/sindresorhus/get-stdin/pull/19/files
  let returnValue = '';

  return new Promise((resolve) => {
    if (stdin.isTTY) {
      resolve(returnValue);
      return;
    }

    const timeout = setTimeout(() => {
      resolve(returnValue);
    }, 100);

    stdin.unref();
    stdin.setEncoding('utf8');

    stdin.on('readable', () => {
      clearTimeout(timeout);
      stdin.ref();

      let chunk;

      while ((chunk = stdin.read())) {
        returnValue += chunk;
      }
    });

    stdin.on('end', () => {
      resolve(returnValue);
    });
  });
}

getStdin().then((string_) => {
  run(string_);
});

function run(stdin) {
  const options = yargs
    .scriptName('djlint')
    .usage(
      `Usage: $0 [OPTIONS] SRC ...

       djLint · lint and reformat HTML templates.`,
    )
    .option('e', {
      alias: 'extension',
      describe: 'File extension to check [default: html]',
      type: 'string',
      demandOption: false,
    })
    .option('h', {
      alias: 'help',
      describe: 'Show this message and exit.',
      type: 'boolean',
      demandOption: false,
    })
    .option('i', {
      alias: 'ignore',
      describe: 'Codes to ignore. ex: "H014,H017"',
      type: 'string',
      demandOption: false,
    })
    .option('reformat', {
      describe: 'Reformat the file(s).',
      type: 'boolean',
      demandOption: false,
    })
    .option('check', {
      describe: 'Check formatting on the file(s).',
      type: 'boolean',
      demandOption: false,
    })
    .option('indent', {
      describe: 'Indent spacing. [default: 4]',
      type: 'int',
      demandOption: false,
    })
    .option('quiet', {
      describe: 'Do not print diff when reformatting.',
      type: 'boolean',
      demandOption: false,
    })
    .option('warn', {
      describe: 'Return errors as warnings.',
      type: 'boolean',
      demandOption: false,
    })
    .option('profile', {
      describe:
        'Enable defaults by template language. ops: django, jinja, nunjucks, handlebars, golang, angular, html [default: html]',
      type: 'string',
      demandOption: false,
    })
    .option('require-pragma', {
      describe:
        "Only format or lint files that starts with a comment with the text 'djlint:on'",
      type: 'boolean',
      demandOption: false,
    })
    .option('lint', {
      describe: 'Lint for common issues. [default option]',
      type: 'boolean',
      demandOption: false,
    })
    .option('use-gitignore', {
      describe: 'Use .gitignore file to extend excludes.',
      type: 'boolean',
      demandOption: false,
    }).argv;

  // Set flags
  const quiet = options.quiet ? '--quiet' : undefined;
  const help = options.h ? '--help' : undefined;
  const warn = options.warn ? '--warn' : undefined;
  const reformat = options.reformat ? '--reformat' : undefined;
  const check = options.check ? '--check' : undefined;
  const require_pragma = options['require-pragma']
    ? '--require-pragma'
    : undefined;
  const lint = options.lint ? '--lint' : undefined;
  const use_gitignore = options['use-gitignore']
    ? '--use-gitignore'
    : undefined;
  const has_stdin = stdin === '' ? options._[0] : '-';

  // Set variables
  const indent = options.indent ? '--indent=' + options.indent : undefined;
  const profile = options.profile ? '--profile=' + options.profile : undefined;
  const ignore = options.ignore ? '--ignore=' + options.ignore : undefined;
  const extension = options.e ? '-e=' + options.extension : undefined;

  const args = [
    has_stdin,
    warn,
    help,
    quiet,
    extension,
    reformat,
    check,
    require_pragma,
    lint,
    use_gitignore,
    indent,
    profile,
    ignore,
  ].filter((x) => {
    return x !== undefined;
  });

  const pyshell = new PythonShell('-m', { args: ['djlint', ...args] });

  if (stdin !== '') {
    pyshell.send(stdin);
  }

  pyshell.on('message', function (message) {
    console.log(clean(message));
  });

  pyshell.on('stderr', function (message) {
    console.log(clean(message));
  });

  pyshell.end(function (error, code) {
    process.exit(code);
  });
}
