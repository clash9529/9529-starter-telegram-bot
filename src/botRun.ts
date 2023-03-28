const PythonShell = require('python-shell').PythonShell;

PythonShell.run('bot.py', null, function (err) {
  if (err) throw err;
  console.log('finished');
});