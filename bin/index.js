
const {spawn} = require('child_process');
const yargs = require("yargs");
const stdin = process.stdin;


function getStdin ()  {
    // https://github.com/sindresorhus/get-stdin/pull/19/files
    let ret = '';

    return new Promise(resolve => {
        if (stdin.isTTY) {
            resolve(ret);
            return;
        }

        const timeout = setTimeout(() => {
            resolve(ret);
        }, 100);

        stdin.unref();
        stdin.setEncoding('utf8');

        stdin.on('readable', () => {
            clearTimeout(timeout);
            stdin.ref();

            let chunk;

            while ((chunk = stdin.read())) {
                ret += chunk;
            }
        });

        stdin.on('end', () => {
            resolve(ret);
        });
    });
};


getStdin().then(str => {run(str)})

function clean(output){
    return output
    .replaceAll("undefined", "")
    .replaceAll("python -m djlint", "djlint")
}

function run(stdin){

    var dataToSend;
    const exitCode=0;
    const options= yargs
     .scriptName('djlint')
     .usage(`Usage: $0 [OPTIONS] SRC ...

        djLint · lint and reformat HTML templates.`)
     .option("e", { alias: "extension", describe: "File extension to check [default: html]", type: "string", demandOption: false })
     .option("i", { alias: "ignore", describe: "Codes to ignore. ex: \"H014,H017\"", type: "string", demandOption: false })
     .option("reformat", { describe: "Reformat the file(s).", type: "boolean", demandOption: false })
     .option("check", { describe: "Check formatting on the file(s).", type: "boolean", demandOption: false })
     .option("indent", { describe: "Indent spacing. [default: 4]", type: "int", demandOption: false })
     .option("quiet", { describe: "Do not print diff when reformatting.", type: "boolean", demandOption: false })
     .option("profile", { describe: "Enable defaults by template language. ops: django, jinja, nunjucks, handlebars, golang, angular, html [default: html]", type: "string", demandOption: false })
     .option("require-pragma", { describe: "Only format or lint files that starts with a comment with the text 'djlint:on'", type: "boolean", demandOption: false })
     .option("lint", { describe: "Lint for common issues. [default option]", type: "boolean", demandOption: false })
     .option("use-gitignore", { describe: "Use .gitignore file to extend excludes.", type: "boolean", demandOption: false })
     .argv;

    // set flags
    const quiet = options.quiet ? '--quiet' : undefined
    const reformat = options.reformat ? '--reformat' : undefined
    const check = options.check ? '--check' : undefined
    const require_pragma = options["require-pragma"] ? '--require-pragma' : undefined
    const lint = options.lint ? '--lint' : undefined
    const use_gitignore = options["use-gitignore"] ? '--use-gitignore' : undefined
    const has_stdin = stdin !== "" ? "-": options._[0]

    // set variables
    const indent = options.indent ? '--indent='+options.indent : undefined
    const profile =options.profile ? '--profile='+options.profile : undefined
    const ignore = options.ignore ? '--ignore='+options.ignore : undefined

    const args = [has_stdin, quiet,reformat,check,require_pragma,lint,use_gitignore, indent, profile, ignore].filter(x => {return x !== undefined})

    const python = spawn('python3', ['-m', 'djlint', ...args], {"cwd": "./src"});

    if(stdin !== ""){
        python.stdin.write(stdin);
        python.stdin.end()
    }

    python.stdout.on('data', function (data) {
        dataToSend += data//.toString();
    });

    python.stderr.on('data', function (data) {
        dataToSend += data//.toString();
    });

    python.on('close', (code) => {
        process.stdout.write(clean(dataToSend))
        process.exit(code)
    });




}
