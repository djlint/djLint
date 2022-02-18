const {spawn} = require('child_process');
var dataToSend;
const python = spawn('python3', ['-m', 'pip', 'install', '--upgrade','--quiet', '-r', '../requirements.txt'], {"cwd": "./src"});


python.stdout.on('data', function (data) {
    dataToSend += data.toString();
});

python.stderr.on('data', function (data) {
    dataToSend += data.toString();
});

python.on('close', (code) => {
    process.stdout.write(dataToSend.replace("undefined",""))
    process.exit(code)
});
