const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit()
}

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    }
  })

  // and load the index.html of the app.
  if (MAIN_WINDOW_VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(MAIN_WINDOW_VITE_DEV_SERVER_URL)
  } else {
    mainWindow.loadFile(path.join(__dirname, `../dist/${MAIN_WINDOW_VITE_NAME}/index.html`))
  }

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  // Start Python backend server
  startPythonServer()

  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.

let pythonServer = null

function startPythonServer() {
  try {
    // Start the Python backend server
    pythonServer = spawn('python', ['../backend/main.py'], {
      cwd: __dirname,
      stdio: ['pipe', 'pipe', 'pipe']
    })

    pythonServer.stdout.on('data', (data) => {
      console.log('Python server stdout:', data.toString())
    })

    pythonServer.stderr.on('data', (data) => {
      console.error('Python server stderr:', data.toString())
    })

    pythonServer.on('close', (code) => {
      console.log('Python server exited with code:', code)
    })

    console.log('Python backend server started')
  } catch (error) {
    console.error('Failed to start Python server:', error)
  }
}

// Handle cleanup when app quits
app.on('before-quit', () => {
  if (pythonServer) {
    pythonServer.kill()
  }
})

// IPC handlers for communication with renderer
ipcMain.on('python-server-ready', (event) => {
  console.log('Frontend is ready to communicate with Python server')
})