import json,os,sys,urllib.request as up
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
def post(p,b):
 r=up.Request(U+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 with up.urlopen(r)as x:return json.load(x)
V=dict(p=100,n=300,b=310,r=500,q=900,k=0)
KN=(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)
DA=(1,1),(1,-1),(-1,1),(-1,-1)
ST=(1,0),(-1,0),(0,1),(0,-1)
AL=DA+ST
C=[12-int(2*abs(f-3.5)+2*abs(r-3.5))for r in range(8)for f in range(8)]
F="abcdefgh"
def parse(fen):
 t=fen.split()
 b=[x for c in"".join(reversed(t[0].split("/")))for x in("."*int(c)if c.isdigit()else c)]
 ep=-1
 if len(t)>3 and t[3]!="-":ep=(int(t[3][1])-1)*8+F.index(t[3][0])
 return b,t[1]=="w",t[2],ep
def sq(b,s,w):
 f,r=s%8,s//8
 for d in KN:
  if 0<=f+d[0]<8 and 0<=r+d[1]<8 and b[(r+d[1])*8+f+d[0]]==("N"if w else"n"):return 1
 pr=r-(1 if w else-1)
 for df in(-1,1):
  if 0<=f+df<8 and 0<=pr<8 and b[pr*8+f+df]==("P"if w else"p"):return 1
 for df,dr in AL:
  tf,tr,i=f+df,r+dr,0
  while 0<=tf<8 and 0<=tr<8:
   c=b[tr*8+tf]
   if c!=".":
    if c.isupper()==w:
     l=c.lower();dg=df and dr
     if l=="q"or(l=="b"if dg else l=="r")or(i==0 and l=="k"):return 1
    break
   tf,tr,i=tf+df,tr+dr,i+1
 return 0
def mk(b,m,w,cs,ep):
 b=b[:]
 s,q,p=m;pc=b[s];b[s]="."
 if pc in"Pp"and b[q]=="."and s%8!=q%8:b[q-(8 if w else-8)]="."
 b[q]=(p.upper()if w else p)if p else pc
 if pc in"Kk"and abs(s%8-q%8)==2:
  a=7 if q%8==6 else 0;b[s-s%8+(5 if a else 3)]=b[s-s%8+a];b[s-s%8+a]="."
 d={4:"KQ",7:"K",0:"Q",60:"kq",63:"k",56:"q"}
 for c in d.get(s,"")+d.get(q,""):cs=cs.replace(c,"")
 return b,cs,(s+q)//2 if pc in"Pp"and abs(q-s)==16 else-1
def gen(b,w,cs,ep):
 for s in range(64):
  p=b[s]
  if p=="."or p.isupper()!=w:continue
  f,r=s%8,s//8;u=p.lower()
  if u=="p":
   d,la,st=(1,7,1)if w else(-1,0,6)
   for tf in(f-1,f,f+1):
    if not 0<=tf<8 or not 0<=r+d<8:continue
    q=(r+d)*8+tf
    if tf==f and b[q]==".":
     if r+d==la:
      for x in"qrbn":yield s,q,x
     else:
      yield s,q,""
      if r==st and b[q+d*8]==".":yield s,q+d*8,""
    elif tf!=f and(b[q]!="."and b[q].isupper()!=w or q==ep):
     if r+d==la:
      for x in"qrbn":yield s,q,x
     else:yield s,q,""
  else:
   for df,dr in KN if u=="n"else DA if u=="b"else ST if u=="r"else AL:
    tf,tr=f+df,r+dr
    while 0<=tf<8 and 0<=tr<8:
     q=tr*8+tf;c=b[q]
     if c==".":yield s,q,""
     else:
      if c.isupper()!=w:yield s,q,""
      break
     if u in"nk":break
     tf,tr=tf+df,tr+dr
  if u=="k":
   o=0 if w else 56
   if s==4+o and b[4+o]==("K"if w else"k"):
    if("K"if w else"k")in cs and b[5+o]==b[6+o]=="."and not sq(b,4+o,not w)and not sq(b,5+o,not w):yield 4+o,6+o,""
    if("Q"if w else"q")in cs and b[3+o]==b[2+o]==b[1+o]=="."and not sq(b,4+o,not w)and not sq(b,3+o,not w):yield 4+o,2+o,""
def lg(b,w,cs,ep):
 o=[]
 for m in gen(b,w,cs,ep):
  nb=mk(b,m,w,cs,ep)[0]
  if not sq(nb,nb.index("K"if w else"k"),not w):o.append(m)
 return o
def ev(b):
 t=0
 for s in range(64):
  p=b[s]
  if p==".":continue
  u=p.lower();r=s//8
  v=V[u]+((r if p.isupper()else 7-r)*6-(s%8 in(0,7))*12 if u=="p"else C[s]if u in"nb"else C[s]//2 if u=="q"else 0)
  t+=v if p.isupper()else-v
 return t
def ng(b,w,d,a,be,cs,ep):
 ms=lg(b,w,cs,ep)
 if not ms:return(-90000-d)if sq(b,b.index("K"if w else"k"),not w)else 0
 if d==0:return ev(b)if w else-ev(b)
 ms.sort(key=lambda m:(V.get(b[m[1]].lower(),0),m[2]=="q"),reverse=True)
 for m in ms:
  nb,nc,ne=mk(b,m,w,cs,ep)
  v=-ng(nb,not w,d-1,-be,-a,nc,ne)
  if v>a:a=v
  if a>=be:break
 return a
def choose(fen,lc):
 b,w,cs,ep=parse(fen);bt,bm=-9e9,min(lc)
 for m in sorted(lg(b,w,cs,ep)):
  u=F[m[0]%8]+str(m[0]//8+1)+F[m[1]%8]+str(m[1]//8+1)+m[2]
  if u not in lc:continue
  nb,nc,ne=mk(b,m,w,cs,ep)
  v=-ng(nb,not w,3,-9e9,9e9,nc,ne)
  if v>bt or(v==bt and u<bm):bt,bm=v,u
 return bm
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
