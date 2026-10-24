"""Rate mined puzzles by how long Stockfish needs to find the answer and write data/puzzles.json.
Usage: python3 tools/rerate_puzzles.py [output.json]"""
import json,glob,os,sys,chess,chess.engine,hashlib,collections
HERE=os.path.dirname(os.path.abspath(__file__))
rows={}
for f in glob.glob(os.path.join(HERE,'mined','puz_*.json')):
    for p in json.load(open(f)):rows[p['fen']]=p
E=chess.engine.SimpleEngine.popen_uci(os.environ.get("STOCKFISH","/usr/games/stockfish"));E.configure({"Threads":1,"Hash":64})
out=[]
for p in rows.values():
    b=chess.Board(p['fen']);best=p['mv'][0];st=None
    seq=[E.analyse(b,chess.engine.Limit(depth=d))['pv'][0].uci() for d in range(1,10)]
    d=9
    while d>=1 and seq[d-1]==best:d-=1
    ds=d+1 if d<9 else 10   # first depth from which the best move is stable (10 = never stable by depth 9)
    n=(len(p['mv'])+1)//2;sac='Sacrifice' in p['th'];mate=p['th'].startswith('Mate')
    h=int(hashlib.md5(p['fen'].encode()).hexdigest()[:4],16)%61-30
    p['r']=max(500,min(2400,520+100*ds+190*(n-1)+(150 if sac else 0)+(60 if mate and n>1 else 0)+h))
    p['ds']=ds;out.append(p)
E.quit()
out.sort(key=lambda p:p['r'])
json.dump([{k:p[k] for k in('fen','mv','r','th')} for p in out],open(sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'..','data','puzzles.json'),'w'),ensure_ascii=False)
c=collections.Counter((p['r']//100)*100 for p in out);print(len(out),sorted(c.items()))
