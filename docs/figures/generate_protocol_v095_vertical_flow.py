from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
W,H=1600,2940
im=Image.new('RGB',(W,H),'#ffffff'); d=ImageDraw.Draw(im)
N='#18222d'; B='#245b85'; G='#52616e'; L='#c9d2d9'; P='#f2f5f7'; PB='#e8f1f7'; WHITE='#ffffff'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def f(s,b=False): return ImageFont.truetype(bold if b else font,s,index=0)
def txt(x,y,s,z=25,b=False,c=N,anchor=None): d.text((x,y),s,font=f(z,b),fill=c,anchor=anchor)
def rect(x,y,w,h,fill=WHITE,stroke=L,r=0):
 if r:d.rounded_rectangle((x,y,x+w,y+h),r,fill=fill,outline=stroke,width=2 if stroke else 0)
 else:d.rectangle((x,y,x+w,y+h),fill=fill,outline=stroke,width=2 if stroke else 0)
def line(x1,y1,x2,y2,c=L,w=2):d.line((x1,y1,x2,y2),fill=c,width=w)
def arrow(x1,y1,x2,y2,c=B,w=4):
 line(x1,y1,x2,y2,c,w);a=math.atan2(y2-y1,x2-x1);k=11;d.polygon([(x2,y2),(x2-k*math.cos(a-.55),y2-k*math.sin(a-.55)),(x2-k*math.cos(a+.55),y2-k*math.sin(a+.55))],fill=c)
def block(x,y,w,h,title,sub=None,fill=P):
 rect(x,y,w,h,fill,L,5);txt(x+w/2,y+13,title,27,True,B,anchor='mt');
 if sub:txt(x+w/2,y+53,sub,21,False,G,anchor='mt')
def textlines(x,y,ls,z=23,step=35,c=N):
 for i,s in enumerate(ls):txt(x,y+i*step,s,z,False,c)
def section(y,h,num,title,tag=''):
 rect(50,y,1500,h,WHITE,L,5);rect(50,y,1500,52,P,None);txt(74,y+9,num+'  '+title,29,True,B)
 if tag:txt(1526,y+14,tag,20,False,G,anchor='ra')
def down(y1,y2):arrow(800,y1+2,800,y2-5,B,5)
def label(x,y,s,z=21):txt(x,y,s,z,True,B)
txt(50,34,'LLMにおける抑制概念と意味的距離',48,True)
txt(52,100,'本実験・統合プロトコル v0.95  ／  2026年11月25日改訂  ／  設計段階・本実験未実施',25,False,G)
line(50,148,1550,148,B,4)
section(168,211,'00','研究目的・リサーチクエスチョン')
txt(78,230,'主題：Avoid X を固定したとき、Cue–X 距離と内部指標はどう関係するか。',29,True)
textlines(82,279,['RQ1  Concept Probe：距離と生成直前の X/Y 相対判別スコアの関係・層別の変化','RQ2  Logit Lens：距離と X/Y 語彙予測マージンの関係、Probeとの一致・乖離','RQ3  副次：Neutral X との距離傾向・傾き差、内部指標と最終出力との対応'],23,31)
down(379,405)
section(405,355,'01','対象概念 X と比較概念 Y の選定','独立Probe評価 → 採択')
xs=[78,440,802,1164]; ww=320
for x,t,s in zip(xs,['候補 X/Y','説明文の準備','独立Probe評価','正式採択・凍結'],['10カテゴリー × 5','学習用／評価用を分離','各層で識別性能を確認','約50の異なる X が目標']):block(x,477,ww,92,t,s)
for x in xs[:-1]:arrow(x+ww+5,523,x+357,523)
label(82,588,'X/Yペアごとに全24層専用の線形Probeを作る')
for i,(s,sub) in enumerate([('X の説明文','名称・別名を原則除外'),('Y の説明文','文型・内容の偏りを監査')]):
 block(82+i*330,626,305,85,s,sub)
arrow(720,665,765,665)
block(775,626,340,85,'線形分類器','Scaler + LogisticRegression',PB)
rect(1140,586,380,149,PB,L,5);txt(1160,595,'L24 暫定採択基準',26,True,B);textlines(1160,632,['AUC ≥ 0.80 ／ BH q ≤ 0.05','独立評価は各ラベル8文以上','初回50組 → 33組暫定通過'],21,29)
txt(82,720,'概念採択はL24のみ。中間層は性能に応じ解釈し、全層通過を要求しない。',21,False,G)
down(760,785)
section(785,473,'02','Cue の生成・意味的距離の測定・採択','本実験とは分離した材料準備')
for x,t,s in zip(xs,['68候補文／X','距離の測定','品質監査','24 Cue／X'],['関連60 + 無関係8','all-mpnet-base-v2','名称露出・事実・重複','関連20 + 無関係4']):block(x,857,ww,88,t,s)
for x in xs[:-1]:arrow(x+ww+5,901,x+357,901)
txt(80,960,'dX = 1 − cosine(emb(Xの定義), emb(Cue))',26,True,B)
txt(1517,965,'dY・dX−dY・文長・文章タイプも保存',22,False,G,anchor='ra')
x0=390;y0=1007;cw=158;rh=35
names=['Very Near','Near','Medium Near','Medium Far','Far','Unrelated']
rows=['構造・特徴','動作・行為','場面・状況','機能・用途']
for j,n in enumerate(names):
 x=x0+j*cw;rect(x,y0,cw-7,43,PB if j<5 else P,L,3);txt(x+(cw-7)/2,y0+10,n,20,True,B if j<5 else G,anchor='mt')
for i,n in enumerate(rows):
 txt(90,y0+53+i*rh,n,22,False,G)
 for j in range(6):
  x=x0+j*cw;rect(x+47,y0+53+i*rh,57,26,PB if j<5 else WHITE,L,4);txt(x+75,y0+53+i*rh,'1文',17,False,B,anchor='mt')
arrow(x0+10,y0+194,x0+5*cw-18,y0+194,B,3)
txt(90,y0+180,'実測 dX：近い → 遠い',19,False,G)
txt(1510,y0+180,'別対照',20,True,G,anchor='ra')
textlines(80,1211,['各距離帯4文の文型均衡は暫定案。距離帯の重なり・間隔・dY分布・自然さを点検。','候補を逐次生成し、合格文を保持。採択理由・ID・距離・version・SHA-256を固定。'],19,24,G)
down(1258,1283)
section(1283,329,'03','材料・条件の凍結 → 本実験入力の構築','v1.0凍結後に実行')
rect(80,1355,690,88,PB,L,5);txt(100,1363,'Avoid X（主条件）',27,True,B);txt(100,1402,'Do not think about {X}.',24)
rect(830,1355,690,88,P,L,5);txt(850,1363,'Neutral X（比較対照）',27,True,B);txt(850,1402,'The word is {X}.',24)
line(425,1443,425,1461,B,3);line(1175,1443,1175,1461,B,3);line(425,1461,1175,1461,B,3);arrow(800,1461,800,1480)
rect(230,1481,1140,55,WHITE,L,5);txt(800,1491,'共通：同じ Cue を提示し、短い語句で回答させる（Cueなしは別対照）',24,True,anchor='mt')
txt(800,1549,'50概念 × (24 Cue + 1 Cueなし) × 2条件 = 2,500 ユニーク入力',32,True,B,anchor='mt')
txt(800,1586,'Cueあり 2,400 ／ Cueなし 100 ／ 生成反復 1 または 5 回（未確定）',21,False,G,anchor='mt')
down(1612,1637)
section(1637,375,'04','Qwen2.5-0.5B-Instruct に入力','GPU推論・固定revision')
label(80,1708,'入力トークン列')
for i,s in enumerate(['指示','X','Cue','…','末尾']):
 x=80+i*106;rect(x,1746,92,48,PB if i==4 else P,L,4);txt(x+46,1754,s,21,True,B if i==4 else G,anchor='mt')
arrow(590,1770,660,1770)
rect(670,1700,320,224,WHITE,L,5);txt(830,1711,'Transformer 24層',25,True,B,anchor='mt')
for i,n in enumerate(['L1','L2','…','L23','L24']):
 yy=1750+i*30;rect(705,yy,250,26,PB if n=='L24' else P,L,3);txt(830,yy-1,n,18,True,B if n=='L24' else G,anchor='mt')
arrow(990,1770,1060,1770);block(1070,1708,445,114,'Hidden State 取得','最後の入力位置 × 全24層 × 896次元',PB)
arrow(830,1924,830,1943);line(830,1943,1055,1943,B,3);arrow(1055,1943,1055,1880);arrow(1055,1880,1067,1880)
block(1070,1839,445,85,'最終出力','短い語句を保存（1回または5回）')
textlines(80,1840,['生成開始直前の位置に固定','内部状態は同一入力につき1回取得','生成反復を独立した内部観測に数えない'],23,33)
txt(80,1961,'凍結済み刺激・Probe・指示・モデルを使用し、推論結果で材料を選び直さない。',22,False,G)
down(2012,2037)
section(2037,425,'05','2種類の内部読み出しと出力評価','CPU分析・主解析はL24')
for x,title,sub in [(78,'Concept Probe（RQ1）','固定線形分類器'),(574,'Logit Lens（RQ2）','固定語彙読み出し'),(1070,'出力評価（RQ3）','重要な副次分析')]:
 rect(x,2108,452,301,WHITE,L,5);rect(x,2108,452,50,PB if x!=1070 else P,None);txt(x+15,2116,title,25,True,B);txt(x+17,2170,sub,22,True,G)
block(96,2209,155,65,'h_l',None);arrow(254,2241,280,2241);block(288,2209,221,65,'w_l^T z + b_l',None,PB)
textlines(96,2290,['X/Y相対 decision score','層専用 scaler・係数を凍結','L22/23 感度・L1–21 探索','AUC／有効概念数も併記'],21,26)
block(592,2209,105,65,'h_l');arrow(701,2241,728,2241);block(735,2209,269,65,'norm → lm_head',None,PB)
textlines(591,2290,['margin_l = log P_l(X) − log P_l(Y)','複数token：teacher forcing','L24のnative logitsと照合','層別軌跡とProbeの対応'],20,27)
block(1088,2209,415,65,'生成テキスト → 採点',None)
textlines(1088,2290,['Xの明示的言及／厳密な概念同定','Cueへの回答妥当性・形式遵守','曖昧・判定不能を区別','同じ入力IDで内部指標と対応'],20,27)
txt(80,2424,'ProbeとLensはX/Y相対情報・語彙投影の測定。思考量や絶対的活性の直接測定ではない。',22,False,G)
down(2462,2487)
section(2487,281,'06','距離との関係を統計的に評価','推定法・CI・多重比較はv1.0で確定')
rect(80,2558,470,143,P,L,5);txt(98,2566,'概念内の連続距離 × 指標',23,True,B)
line(125,2670,475,2670,G,2);line(125,2670,125,2603,G,2);txt(300,2676,'dX（関連20 Cueのみ）',18,False,G,anchor='mt');txt(144,2601,'スコア',17,False,G);txt(315,2630,'実測値を図示予定',19,False,G,anchor='mt')
rect(570,2558,465,143,P,L,5);txt(590,2566,'比較・調整',23,True,B);textlines(590,2604,['Avoid X と Neutral X の傾き差','dY調整：偏順位相関／回帰候補','文長・文型などの感度分析'],21,28)
rect(1055,2558,465,143,P,L,5);txt(1075,2566,'全体・層別の推定',23,True,B);textlines(1075,2604,['概念別傾き → 分布／全体推定','階層回帰・概念単位の再標本化候補','L1–24：AUC・有効概念数を併記'],20,28)
txt(80,2722,'無関係・Cueなしは主距離回帰に含めない。距離の純粋な因果効果は主張しない。',22,False,G)
line(50,2795,1550,2795,B,3);txt(52,2807,'現在地と次の工程',28,True,B)
textlines(52,2845,['既存10概念の再分析・500回答の評価 → 追加Probe探索 → 本番Cue準備・人手監査','採択・統計・生成反復数・実行条件を確定 → v1.0凍結 → GPU本実験 → CPU解析'],23,34)
txt(1548,2911,'出典：GraduationThesis / docs/main_experiment_protocol_v0_95.md',17,False,G,anchor='ra')
im.save(Path(__file__).with_name('protocol_v095_vertical_flow.png'),optimize=True)
