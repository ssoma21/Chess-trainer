import chess,chess.engine,random,json,hashlib,sys,time,os
"""Mine tactics puzzles with a native Stockfish + python-chess.
Usage: python3 tools/mine_puzzles.py SEED SECONDS TARGET   (writes tools/mined/puz_SEED.json)
Then run tools/rerate_puzzles.py to merge and rate them into data/puzzles.json."""
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"mined");os.makedirs(OUT,exist_ok=True)
seed=int(sys.argv[1]);TL=float(sys.argv[2]);TARGET=int(sys.argv[3]);random.seed(seed)
E=chess.engine.SimpleEngine.popen_uci(os.environ.get("STOCKFISH","/usr/games/stockfish"));E.configure({"Threads":1,"Hash":64})
LIM=chess.engine.Limit(depth=12);SCAN=chess.engine.Limit(depth=9);V={1:1,2:3,3:3,4:5,5:9,6:20}
lines=[l.split("|")[2].split() for l in json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"data","opening_lines.json")))]
cp=lambda s:s.score(mate_score=10000)
rel=lambda i:i["score"].relative
def opening(b):
    for s in random.choice(lines)[:random.randint(4,14)]:
        try:b.push_san(s)
        except Exception:break
def val(b,sq):
    p=b.piece_at(sq);return V[p.piece_type] if p else 0
def build(b):
    solver=b.turn;line=[];b2=b.copy();first=None
    for k in range(3):
        inf=E.analyse(b2,LIM,multipv=2);bst=inf[0]
        if "pv" not in bst:break
        bs=cp(rel(bst));sec=cp(rel(inf[1])) if len(inf)>1 else -10000
        if k>0 and not(bs>=250 and bs-sec>=250):break
        mv=bst["pv"][0]
        if k==0:first=(b2.copy(),mv)
        line.append(mv);b2.push(mv)
        if b2.is_game_over():break
        r=E.analyse(b2,LIM)
        if "pv" not in r:break
        line.append(r["pv"][0]);b2.push(r["pv"][0])
        if b2.is_game_over():break
    if len(line)%2==0:line=line[:-1]
    if not line:return None
    b3=b.copy()
    for m in line:b3.push(m)
    mate=b3.is_checkmate()
    if not mate:
        r=E.analyse(b3,LIM)
        if -cp(rel(r))<250:return None
    n=(len(line)+1)//2
    b0,m0=first;cap=val(b0,m0.to_square) if b0.is_capture(m0) else 0;pc=val(b0,m0.from_square)
    b1=b0.copy();b1.push(m0);att=b1.attackers(not solver,m0.to_square)
    sac=bool(att) and pc-cap>=2 and not b1.is_checkmate()
    quiet=not b0.is_capture(m0) and not b0.gives_check(m0)
    h=int(hashlib.md5(b.fen().encode()).hexdigest()[:4],16)%81-40
    r=650+220*(n-1)+(100 if mate and n>1 else 0)+(250 if sac else 0)+(120 if quiet else 0)+h
    th=("Mate in %d"%n if mate else "Win material")+(" · Sacrifice" if sac else "")
    return dict(fen=b.fen(),mv=[m.uci() for m in line],r=max(500,min(2400,r)),th=th)
def verify(p):
    b=chess.Board(p["fen"]);inf=E.analyse(b,chess.engine.Limit(depth=16),multipv=2)
    if inf[0]["pv"][0].uci()!=p["mv"][0]:return False
    bs=cp(rel(inf[0]));sec=cp(rel(inf[1])) if len(inf)>1 else -10000
    return bs>=250 and bs-sec>=200
puz=[];seen=set();easy=0;t0=time.time()
while len(puz)<TARGET and time.time()-t0<TL:
    b=chess.Board();opening(b);prev=None
    for ply in range(random.randint(10,40)):
        if b.is_game_over() or time.time()-t0>TL:break
        inf=E.analyse(b,SCAN,multipv=2);bs=cp(rel(inf[0]));sec=cp(rel(inf[1])) if len(inf)>1 else -10000
        if prev is not None and -prev<=150 and bs>=250 and bs-sec>=250 and len(b.piece_map())>=7:
            p=build(b.copy())
            if p and p["fen"] not in seen and verify(p):
                bb=chess.Board(p["fen"]);seq=[E.analyse(bb,chess.engine.Limit(depth=d))["pv"][0].uci() for d in range(1,6)]
                hard=seq[0]!=p["mv"][0] or seq[1]!=p["mv"][0] or len(p["mv"])>1 or "Sacrifice" in p["th"]
                if hard or easy<30:
                    if not hard:easy+=1
                    seen.add(p["fen"]);puz.append(p)
        prev=bs
        if random.random()<0.18:mv=random.choice(list(b.legal_moves))
        else:mv=E.play(b,chess.engine.Limit(time=0.02),options={"Skill Level":random.choice([1,3,5,8])}).move
        b.push(mv)
    json.dump(puz,open(os.path.join(OUT,"puz_%d.json"%seed),"w"))
json.dump(puz,open(os.path.join(OUT,"puz_%d.json"%seed),"w"));E.quit();print("done",seed,len(puz))
