#!/usr/bin/env bash
# Builds dist/ChessTrainer-Setup.exe (Electron app + NSIS installer) on Linux/macOS/WSL.
# Needs: curl, unzip, makensis (Ubuntu: sudo apt install nsis unzip curl), Python 3 + Pillow.
# Set ELECTRON_ZIP=/path/to/electron-v33.2.0-win32-x64.zip to skip the download.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; HERE="$ROOT/platforms/windows"; W="$ROOT/dist/windows"
VER="$(cat "$ROOT/VERSION")"; EV="33.2.0"
[ -f "$ROOT/dist/chess-trainer-offline.html" ] || python3 "$ROOT/tools/build_offline.py"
python3 "$ROOT/tools/make_icons.py" >/dev/null
mkdir -p "$ROOT/dist/cache"; ZIP="${ELECTRON_ZIP:-$ROOT/dist/cache/electron-v$EV-win32-x64.zip}"
[ -f "$ZIP" ] || curl -fL -o "$ZIP" "https://github.com/electron/electron/releases/download/v$EV/electron-v$EV-win32-x64.zip"
rm -rf "$W"; mkdir -p "$W/app"
unzip -q "$ZIP" -d "$W/app"
mv "$W/app/electron.exe" "$W/app/ChessTrainer.exe"
rm -f "$W/app/resources/default_app.asar"
find "$W/app/locales" -name '*.pak' ! -name 'en-US.pak' -delete     # keep English only (smaller)
mkdir -p "$W/app/resources/app"
cp "$ROOT/dist/chess-trainer-offline.html" "$W/app/resources/app/index.html"
cp "$HERE/main.js" "$W/app/resources/app/main.js"
cp "$ROOT/dist/icons/icon-192-rounded.png" "$W/app/resources/app/icon.png"
cp "$ROOT/dist/icons/icon.ico" "$W/app/icon.ico"; cp "$ROOT/dist/icons/icon.ico" "$W/icon.ico"
printf '{"name":"chess-trainer","productName":"Chess Trainer","version":"%s","main":"main.js"}\n' "$VER" > "$W/app/resources/app/package.json"
cp "$ROOT/LICENSE" "$W/app/LICENSE-ChessTrainer.txt"; cp "$ROOT/THIRD_PARTY_NOTICES.md" "$W/app/THIRD_PARTY_NOTICES.md"
cp "$HERE/installer.nsi" "$W/"
(cd "$W" && makensis -V1 -DVERSION="$VER" installer.nsi)
mv "$W/ChessTrainer-Setup.exe" "$ROOT/dist/ChessTrainer-Setup.exe"; echo "built dist/ChessTrainer-Setup.exe ($VER)"
