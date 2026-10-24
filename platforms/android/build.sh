#!/usr/bin/env bash
# Builds dist/ChessTrainer.apk (signed with a locally generated debug key).
# Needs: JDK, aapt, zipalign, apksigner, dalvik-exchange, Android API 23 android.jar
#   Ubuntu: sudo apt install default-jdk-headless aapt zipalign apksigner dalvik-exchange libandroid-23-java
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; HERE="$ROOT/platforms/android"; W="$ROOT/dist/android"
VER="$(cat "$ROOT/VERSION")"; CODE="$(echo "$VER" | awk -F. '{print $1*100+$2*10+($3+0)}')"
AJ="${ANDROID_JAR:-/usr/lib/android-sdk/platforms/android-23/android.jar}"
[ -f "$ROOT/dist/chess-trainer-offline.html" ] || python3 "$ROOT/tools/build_offline.py"
python3 "$ROOT/tools/make_icons.py" >/dev/null
rm -rf "$W"; mkdir -p "$W/assets" "$W/res/drawable-xxhdpi" "$W/classes" "$W/src/com/chesstrainer/app"
cp "$ROOT/dist/chess-trainer-offline.html" "$W/assets/index.html"
cp "$ROOT/dist/icons/icon-192-rounded.png" "$W/res/drawable-xxhdpi/ic_launcher.png"
cp "$HERE/MainActivity.java" "$W/src/com/chesstrainer/app/"
sed "s/__VERSION_NAME__/$VER/; s/__VERSION_CODE__/$CODE/" "$HERE/AndroidManifest.xml" > "$W/AndroidManifest.xml"
cd "$W"
javac --release 8 -cp "$AJ" -d classes src/com/chesstrainer/app/MainActivity.java
dalvik-exchange --dex --min-sdk-version=21 --output=classes.dex classes
aapt package -f -M AndroidManifest.xml -S res -A assets -I "$AJ" -F unsigned.apk
aapt add unsigned.apk classes.dex >/dev/null
zipalign -f -p 4 unsigned.apk aligned.apk
KS="$HERE/debug.keystore"   # gitignored; generated on first run
[ -f "$KS" ] || keytool -genkeypair -keystore "$KS" -alias chess -keyalg RSA -keysize 2048 -validity 10000 -storepass android -keypass android -dname "CN=Chess Trainer" >/dev/null 2>&1
apksigner sign --ks "$KS" --ks-pass pass:android --key-pass pass:android --out "$ROOT/dist/ChessTrainer.apk" aligned.apk
apksigner verify "$ROOT/dist/ChessTrainer.apk" && echo "built dist/ChessTrainer.apk ($VER)"
