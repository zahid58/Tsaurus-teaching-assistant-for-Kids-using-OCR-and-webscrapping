// Modules to control application life and create native browser window
const {app, BrowserWindow} = require('electron')

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {
  // Create the browser window.
    mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    resizable: false,
    frame: false,
    webPreferences: {
      nodeIntegration: true
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('gui/gui.html')

  // Open the DevTools.
 mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
    app.quit()
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.



//this function in typedInput.html
function processWord()
{   
  //alert("in process word");
  location.replace("output.html");

    
    /*for(var i=0;i<imageurls.length;i++)
    {
      var img = document.createElement("img");
      img.src = imageurls[i];
      document.getElementById("images_").appendChild(img);
    }*/
}


//***************************************


//helper method
function parseString(str) {
  return str.replace(/#&#/g, '<br>')
}

function callPython()
{

  const loader = document.getElementById("loader");
  loader.className += " show";

  const {PythonShell} = require("python-shell");
  const path = require("path");
  var word = document.getElementById("input1").value;
  document.getElementById("input1").value = "";
  const script_path = path.join(__dirname,'../backend/');
  let options = {
    mode: 'text',
    pythonPath: "G:/anaconda3/python.exe",
    scriptPath: "G:/PROJECTS/SoftDevProject/tsaurusElectron/backend",
    args: [word]
  }
  console.log(options);
  let pyWord = new PythonShell('processWord.py',options) ;
  pyWord.on('message',function(message){
    location.replace("output.html");
  })
}



//this function in OUTPUT.HTML
function processOutput()
{
  var dictionaryString ="";
  var encyclopediaString = "";
  var imageurls =[]; 
  //need to make these above variables all scope
  const fs = require("fs");
  var filepath = "temp/dictionary.txt";
  try{
    dictionaryString = fs.readFileSync(filepath, 'utf-8');
    dictionaryString = parseString(dictionaryString);
    //alert(dictionaryString);
    document.getElementById("dictionary").innerHTML += dictionaryString;
  }
  catch(err)
  {
    alert(err);
  }
  filepath = "temp/description.txt";
  try{
    encyclopediaString = fs.readFileSync(filepath,'utf-8');
    encyclopediaString = parseString(encyclopediaString);
    document.getElementById("encyclopedia").innerHTML += encyclopediaString;
    //alert(encyclopediaString);
  }
  catch(err)
  {
    alert(err);
  }
  
}


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