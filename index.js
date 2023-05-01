
var PythonShell = require('python-shell');


PythonShell.run('bot.py', null).then(messages=>{
    console.log('finished');
  });