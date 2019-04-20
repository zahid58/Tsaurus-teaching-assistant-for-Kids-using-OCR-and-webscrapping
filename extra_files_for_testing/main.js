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
  console.log("in processWordTypedInput---"); 
  var word=document.getElementById("input1").value;
  localStorage.setItem("word",word); 
  callPython(word);

}


function processWordOcrInput(word)
{
  localStorage.setItem("word",word);
  callPython(word);   
}


//call processWord.py
function callPython(word)
{
  console.log("in callPython---");
  const loader = document.getElementById("loader");
  loader.className += " show";

  const db = require('better-sqlite3')('G:/PROJECTS/SoftDevProject/tsauruswithsqlite/temp/sqlite2.db');
  var row = undefined;
  try{
    row = db.prepare('select * from word_table where word=?;').get(word);
    console.log(row);
  }
  catch{
    db.prepare("CREATE TABLE IF NOT EXISTS word_table (word text primary key,dic_text  text,speech_type text,description text,img_url1 text,img_url2 text,img_url3 text,img_url4 text,img_url5 text,img_url6 text,freq_of_srch number);");
    row = db.prepare('select * from word_table where word =?;').get(word);
    console.log(row);
  }
  if(typeof row == 'undefined')
  {
    
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
    
    var status = false;

    pyWord.on('message',function(message){
        console.log(message);
        status = true;
        one();
    })
    
  
    
    
    ////// make this synchronous!
        function one(){
            console.log("in one....");
            if(status==true){
            const db = require('better-sqlite3')('G:/PROJECTS/SoftDevProject/tsauruswithsqlite/temp/sqlite2.db');  
            var row = undefined;
            row = db.prepare('select * from word_table where word=?;').get(word);
            if(typeof row =='undefined')
            {
              processOutputError();
            }
            else{
              processOutput(row);
            }
            two();
          }
          status=false;
        }
      }    
      else{
          processOutput(row);
          two();
      }
      function two(){
        if(status==true){
        console.log("processing ouput finished ... now showing output!");
        const output= document.getElementById("output");
        output.className+= " show";
        }
        status= false;
      }
}

// error output 
function processOutputError(){
  console.log("in processOutputError---");
  document.getElementById("suppliedWord").innerHTML = localStorage.getItem("word");
  localStorage.removeItem("word");
  document.getElementById("dictionary").innerHTML+= "Check your Internet Connection !!!"
  document.getElementById("encyclopedia").innerHTML+= "Ooops! Mr.Tsaurus could not reach the net !!! ";
  for(var i=0;i<6;i++)
  {
    var x = document.createElement("IMG");
    x.setAttribute("src", "../temp/errorImage.jpg");
    x.setAttribute("width", "200");
    x.setAttribute("height","140");
    x.setAttribute("style","margin:4px;");
    document.getElementById("images_").appendChild(x);
  }
}

// optimum output
function processOutput(row)
{
  console.log("in processOutput---");
  document.getElementById("suppliedWord").innerHTML = row.word;
  localStorage.removeItem("word");
  document.getElementById("dictionary").innerHTML+=row.dic_text;
  document.getElementById("encyclopedia").innerHTML+=row.description;
  var imageurls   = [ row.img_url1, row.img_url2, row.img_url3, row.img_url4, row.img_url5, row.img_url6 ];  
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


function callDetect(){

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

//called from ocrInput.html
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