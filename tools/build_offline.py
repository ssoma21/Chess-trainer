#!/usr/bin/env python3
"""Build dist/chess-trainer-offline.html: one self-contained file (chess.js + Stockfish inlined)."""
import base64, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p, m="r": open(os.path.join(ROOT, p), m, **({"encoding": "utf-8"} if m == "r" else {})).read()
src = rd("src/index.template.html")
puzzles = json.load(open(os.path.join(ROOT, "data/puzzles.json"), encoding="utf-8"))
pz = json.dumps(["%s|%s|%d|%s" % (p["fen"], " ".join(p["mv"]), p["r"], p["th"]) for p in puzzles], ensure_ascii=False)
assert src.count("__PUZZLES__") == 1
src = src.replace("__PUZZLES__", pz)
sfj = rd("vendor/stockfish/stockfish.js")
patch = "var Module={wasmBinaryFile:WasmPath}"
assert sfj.count(patch) == 1
sfj = sfj.replace(patch, "var Module={wasmBinaryFile:WasmPath,wasmBinary:self.__WB}")
sfw = base64.b64encode(rd("vendor/stockfish/stockfish.wasm", "rb")).decode()
tag = '<script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>'
assert src.count(tag) == 1
out = src.replace(tag, "<script>\n" + rd("vendor/chess.js/chess.js") + "\n</script>\n"
                  '<script type="text/plain" id="sfj">' + sfj + "</script>\n"
                  '<script type="text/plain" id="sfw">' + sfw + "</script>")
os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
dst = os.path.join(ROOT, "dist", "chess-trainer-offline.html")
open(dst, "w", encoding="utf-8").write(out)
print("wrote", dst, len(out), "bytes,", len(puzzles), "puzzles")
