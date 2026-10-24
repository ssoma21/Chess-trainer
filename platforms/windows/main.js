const { app, BrowserWindow, Menu } = require("electron");
const path = require("path");
function createWindow() {
  Menu.setApplicationMenu(null);
  const w = new BrowserWindow({
    width: 1000, height: 920, minWidth: 420, minHeight: 600,
    backgroundColor: "#262522", title: "Chess Trainer",
    icon: path.join(__dirname, "icon.png"), autoHideMenuBar: true,
    webPreferences: { contextIsolation: true, nodeIntegration: false }
  });
  w.loadFile(path.join(__dirname, "index.html"));
}
app.whenReady().then(createWindow);
app.on("window-all-closed", () => app.quit());
