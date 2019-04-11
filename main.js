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


//***************************************


//this function in typedInput.html
function processWordTypedInput()
{   
  var word=document.getElementById("input1").value;
  localStorage.setItem("word",word);
  callPython();
}
function processWordOcrInput(word)
{
  localStorage.setItem("word",word);
  callPython();
}


//call processWord.py
function callPython()
{
  
  const loader = document.getElementById("loader");
  loader.className += " show";
  var word = localStorage.getItem("word");
  const {PythonShell} = require("python-shell");
  const path = require("path");
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
  document.getElementById("suppliedWord").innerHTML = localStorage.getItem("word");
  localStorage.removeItem("word");
  var dictionaryString ="";
  var encyclopediaString = "";
  //need to make these above variables all scope
  const fs = require("fs");
  var filepath = "temp/dictionary.txt";
  try{
    dictionaryString = fs.readFileSync(filepath, 'utf-8');
    document.getElementById("dictionary").innerHTML += dictionaryString;
  }
  catch(err)
  {
    alert(err);
  }
  filepath = "temp/description.txt";
  try{
    encyclopediaString = fs.readFileSync(filepath,'utf-8');
    document.getElementById("encyclopedia").innerHTML += encyclopediaString;
  }
  catch(err)
  {
    alert(err);
  }
  
}

function loadOutputImages()
{
  const fs = require("fs");
  var filepath = "temp/imageurls.json";
  try{
    var imageurls = JSON.parse(fs.readFileSync(filepath));
    imageurls = Object.keys(imageurls)
    
    
    for(var i=0;i<imageurls.length;i++)
    {
      var x = document.createElement("IMG");
      x.setAttribute("src", imageurls[i]);
      x.setAttribute("width", "200");
      x.setAttribute("height","140");
      x.setAttribute("style","margin:4px;");
      document.getElementById("images_").appendChild(x);
    }
  }
  catch(err)
  {
     alert(err);
  }
}



function callDetect(){
// call the python OCR program
// go to a page thats supposed to run when ocr runs
// then call ocr
// wait for message
// load ocrInput.html 
// hopefully it will work
  const loader = document.getElementById("loader");
  loader.className += " show";
  const {PythonShell} = require("python-shell");
  const path = require("path");
  const script_path = path.join(__dirname,'../backend/');
  let options = {
    mode: 'text',
    pythonPath: "G:/anaconda3/python.exe",
    scriptPath: "G:/PROJECTS/SoftDevProject/tsaurusElectron/backend",
  }
  console.log(options);
  let pyWord = new PythonShell('ocrInput.py',options) ;
  pyWord.on('message',function(message){
    location.replace("ocrInput.html");
  })
}

function getDetectedWords()
{
  const fs = require("fs");
  var filepath = "temp/detected.json";
  try{
    var words = JSON.parse(fs.readFileSync(filepath));
    words = Object.keys(words)
    
    for(var i=0;i<words.length;i++)
    {
      var x = document.createElement("button");
      x.setAttribute("class", "button");
      x.setAttribute("style", "width:auto; height:auto;font-size:auto;padding:5px;margin:5px;");
      x.setAttribute("onclick","processWordOcrInput('"+words[i]+"');");
      var buttoninside = "<span>"+words[i]+"</span>";
      x.innerHTML = buttoninside;
      document.getElementById("menu").appendChild(x);
    }
  }
  catch(err)
  {
    //create a text saying ..sorry i could not detect anything..
     alert(err);
  }
}



/*imageurls.forEach(function(item){
      
    });*/

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

/*
<img src="1558.jpg" width="200px" > 

*/
/*
<div id="loader">
    <img id="dinosaur" alt="mr. tsaurus image" src= "tsaurus.png" class="coverImage">
    <img id="loadingGif" alt="loading gif image" src="loadingGif.gif" class="loading">
    <p1 id="text1" style="right: 140px; top: 320px;text-align: center;">
    capture some text in the camera window....
    <br/><br/>
    <b>Mr. Tsaurus</b> is looking for <b>words</b> in the camera window....
    </p1>
</div>
*/