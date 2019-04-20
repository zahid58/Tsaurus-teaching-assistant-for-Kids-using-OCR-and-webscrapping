/*
python path --
G:\anaconda3\python36.zip
G:\anaconda3\DLLs
G:\anaconda3\lib
G:\anaconda3
G:\anaconda3\lib\site-packages
G:\anaconda3\lib\site-packages\win32
G:\anaconda3\lib\site-packages\win32\lib
G:\anaconda3\lib\site-packages\Pythonwin
*/

var {PythonShell} = require('python-shell');
var options = {
    mode:'text',
    pythonPath: 'G:/anaconda3/python.exe',
    scriptPath: 'G:/PROJECTS/SoftDevProject/tsaurusElectron'
}
let pyWord = new PythonShell('pythonFile.py',options) ;
var msg = "";
pyWord.on('message',function(message){
    msg = message;
})
console.log(msg);