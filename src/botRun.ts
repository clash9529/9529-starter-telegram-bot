const PythonShell = require('python-shell').PythonShell;

while(true){
  PythonShell.run('bot.py', null, function (err:any) {
    if (err) throw err;
    console.log('finished');
  });

}
  