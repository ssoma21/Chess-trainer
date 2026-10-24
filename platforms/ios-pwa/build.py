#!/usr/bin/env python3
"""Build dist/ChessTrainer-iPhone-PWA.zip: an installable offline web app (host it over https, then Safari > Share > Add to Home Screen)."""
import json, os, shutil, subprocess, sys, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VER = open(os.path.join(ROOT, "VERSION")).read().strip()
if not os.path.exists(os.path.join(ROOT, "dist/chess-trainer-offline.html")): subprocess.check_call([sys.executable, os.path.join(ROOT, "tools/build_offline.py")])
subprocess.check_call([sys.executable, os.path.join(ROOT, "tools/make_icons.py")], stdout=subprocess.DEVNULL)
out = os.path.join(ROOT, "dist", "pwa"); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
for n in ("icon-180.png", "icon-192.png", "icon-512.png"): shutil.copy(os.path.join(ROOT, "dist/icons", n), out)
html = open(os.path.join(ROOT, "dist/chess-trainer-offline.html"), encoding="utf-8").read()
title = "<title>Chess Opening Trainer</title>"; assert html.count(title) == 1
html = html.replace(title, title + '''
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Chess Trainer">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#262522">''')
i = html.rindex("</body>")
html = html[:i] + '<script>if("serviceWorker"in navigator&&location.protocol.indexOf("http")==0)addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){})})</script>\n' + html[i:]
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
manifest = {"name": "Chess Opening Trainer", "short_name": "Chess Trainer", "start_url": "./", "scope": "./", "display": "standalone", "orientation": "portrait",
            "background_color": "#262522", "theme_color": "#262522",
            "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                      {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
json.dump(manifest, open(os.path.join(out, "manifest.webmanifest"), "w"))
open(os.path.join(out, "sw.js"), "w").write('''const C="chess-trainer-v%s",F=["./","index.html","manifest.webmanifest","icon-180.png","icon-192.png","icon-512.png"];
self.addEventListener("install",e=>e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting())));
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!=C).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{if(e.request.method!="GET")return;e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request)))});
''' % VER)
zp = os.path.join(ROOT, "dist", "ChessTrainer-iPhone-PWA.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for n in sorted(os.listdir(out)): z.write(os.path.join(out, n), n)
print("built", zp, "(%s)" % VER)
