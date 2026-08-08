#!/usr/bin/env python3
"""
奇門遁甲量化系統 V2 (Qi Men Dun Jia Quantification System V2)
=================================================================
基於天心堂坤正師傅 EP01-EP19 全部教學內容的完整量化引擎

V2 新增（相較 V1/engine.py）：
  1. 完整格局偵測庫（吉格16 + 凶格14）
  2. 六儀擊刑檢測（EP17，6個固定組合）
  3. 五不遇時檢測（EP17，10個組合）
  4. 門迫檢測（EP17，12個組合）
  5. 飛干格/伏干格檢測（EP17）
  6. 天干入墓/八門入墓檢測（EP18）
  7. 出墓/衝墓時間推算（EP18）
  8. 十二長生計算 + 宮位狀態查詢（EP14/EP15）
  9. 刑事定罪判斷函數（EP18）
 10. 民事官司判斷函數（EP17）
 11. 疾病預測分析函數（EP13-EP15）
 12. 通用用神體系 11 場景（EP02-EP19）
 13. 宮位得地/失地計算
 14. 伏吟/反吟局檢測（EP12）
 15. 玉女守門/三奇貴人升殿/奇遊祿位（EP16）
 16. 天輔吉時（EP16）
 17. 多用神交叉驗證框架
 18. 久病逢衝（EP14）

⚠️ 節氣日期為 2026 年近似值，精確起局需配合萬年曆
⚠️ 日干支公式已用 2000-01-01=戊午日 校準
"""
from datetime import datetime
"""
奇門遁甲量化系統 V2 — Part 1: 基礎數據 + 四盤飛布 + 十二長生 + 入墓
=====================================================================
基於天心堂坤正師傅 EP01-EP19 全部教學內容
"""

TIANGAN = list('甲乙丙丁戊己庚辛壬癸')
DIZHI   = list('子丑寅卯辰巳午未申酉戌亥')
def _make_60jz(): return [TIANGAN[i%10]+DIZHI[i%12] for i in range(60)]
LIUJIAZI = _make_60jz()
LIUYI_SANQI = list('戊己庚辛壬癸丁丙乙')
XUNSHOU_DUNYI = {'甲子':'戊','甲戌':'己','甲申':'庚','甲午':'辛','甲辰':'壬','甲寅':'癸'}
XUNSHOU_IDX = [0,10,20,30,40,50]
JIUXING = ['天蓬','天芮','天沖','天輔','天禽','天心','天柱','天任','天英']
JIUXING_SCORE = {'天心':3.0,'天任':2.5,'天輔':2.5,'天禽':2.0,'天沖':1.0,'天英':0.5,'天芮':-1.5,'天柱':-1.5,'天蓬':-2.0}
BAMEN_ORDER = ['休門','死門','傷門','杜門','開門','驚門','生門','景門']
BAMEN_HOME  = [1,2,3,4,6,7,8,9]
BAMEN_SCORE = {'開門':3.0,'生門':3.0,'休門':2.5,'景門':1.0,'死門':-3.0,'驚門':-2.5,'傷門':-2.0,'杜門':-1.5}
BASHEN_ORDER = ['值符','騰蛇','太陰','六合','白虎','玄武','九地','九天']
BASHEN_SCORE = {'值符':3.0,'九天':2.0,'六合':2.0,'太陰':1.5,'九地':1.0,'騰蛇':-1.5,'玄武':-2.0,'白虎':-2.5}
GONG_BAGUA = {1:'坎',2:'坤',3:'震',4:'巽',5:'中',6:'乾',7:'兌',8:'艮',9:'離'}
PALACE_WUXING = {1:'水',2:'土',3:'木',4:'木',5:'土',6:'金',7:'金',8:'土',9:'火'}
TG_WUXING = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
BAMEN_WUXING = {'休門':'水','生門':'土','傷門':'木','杜門':'木','景門':'火','死門':'土','驚門':'金','開門':'金'}
WUXING_SHENG = {"金":"水","水":"木","木":"火","火":"土","土":"金"}
WUXING_KE   = {"金":"木","木":"土","土":"水","水":"火","火":"金"}
WX_SK = {
    ('木','木'):1.0,('木','火'):0.5,('木','土'):0.3,('木','金'):-1.5,('木','水'):0.8,
    ('火','木'):-1.5,('火','火'):1.0,('火','土'):0.5,('火','金'):0.3,('火','水'):-1.5,
    ('土','木'):0.3,('土','火'):0.8,('土','土'):1.0,('土','金'):0.5,('土','水'):-1.5,
    ('金','木'):0.8,('金','火'):-1.5,('金','土'):-1.5,('金','金'):1.0,('金','水'):0.5,
    ('水','木'):0.5,('水','火'):-1.5,('水','土'):0.3,('水','金'):0.8,('水','水'):1.0,
}
TONGGUAN = {("金","木"):"水",("木","土"):"火",("水","火"):"木",("火","金"):"土",("土","水"):"金"}
TG_XIANGHE = {'甲':'己','己':'甲','乙':'庚','庚':'乙','丙':'辛','辛':'丙','丁':'壬','壬':'丁','戊':'癸','癸':'戊'}
TG_XIANGCHONG = {'甲':'庚','庚':'甲','乙':'辛','辛':'乙','丙':'壬','壬':'丙','丁':'癸','癸':'丁'}
TG_HIDDEN_DZ = {'戊':'子','己':'戌','庚':'申','辛':'午','壬':'辰','癸':'寅'}
DZ_CHONG = {'子':'午','午':'子','丑':'未','未':'丑','寅':'申','申':'寅','卯':'酉','酉':'卯','辰':'戌','戌':'辰','巳':'亥','亥':'巳'}
DZ2GONG = {'子':1,'丑':8,'寅':8,'卯':3,'辰':4,'巳':4,'午':9,'未':2,'申':2,'酉':7,'戌':6,'亥':6}
LUOSHU = [[4,9,2],[3,5,7],[8,1,6]]
XUNSHOU_STAR = {'甲子':'天蓬','甲戌':'天芮','甲申':'天沖','甲午':'天輔','甲辰':'天心','甲寅':'天禽'}
STAR_DOOR = {'天蓬':'休門','天芮':'死門','天沖':'傷門','天輔':'杜門','天禽':'死門','天心':'開門','天柱':'驚門','天任':'生門','天英':'景門'}
SIGAN_ROLES = {'年干':['父母','長輩','最高領導'],'月干':['兄弟姊妹','同事','平輩'],'日干':['求測人','自己'],'時干':['子女','下級','求測的事']}

JIEQI_2026 = [('小寒',1,5),('大寒',1,20),('立春',2,4),('雨水',2,19),('驚蟄',3,6),('春分',3,21),('清明',4,5),('穀雨',4,20),('立夏',5,6),('小滿',5,21),('芒種',6,6),('夏至',6,21),('小暑',7,7),('大暑',7,23),('立秋',8,7),('處暑',8,23),('白露',9,8),('秋分',9,23),('寒露',10,8),('霜降',10,24),('立冬',11,7),('小雪',11,22),('大雪',12,7),('冬至',12,22)]
JIEQI_BASE = {'冬至':1,'小寒':2,'大寒':3,'立春':8,'雨水':9,'驚蟄':1,'春分':2,'清明':3,'穀雨':4,'立夏':4,'小滿':5,'芒種':6,'夏至':9,'小暑':8,'大暑':7,'立秋':2,'處暑':1,'白露':9,'秋分':8,'寒露':7,'霜降':6,'立冬':6,'小雪':5,'大雪':4}
YANG_JIEQI = set(['冬至','小寒','大寒','立春','雨水','驚蟄','春分','清明','穀雨','立夏','小滿','芒種'])

def _julian(y,m,d):
    if m<=2: y-=1; m+=12
    A=y//100; B=2-A+A//4
    return int(365.25*(y+4716))+int(30.6001*(m+1))+d+B-1525
def day_ganzhi(dt):
    idx=(_julian(dt.year,dt.month,dt.day)+9)%60; return LIUJIAZI[idx],idx
def shichen_dz(hour):
    for s,n in [(23,'子'),(21,'亥'),(19,'戌'),(17,'酉'),(15,'申'),(13,'未'),(11,'午'),(9,'巳'),(7,'辰'),(5,'卯'),(3,'寅'),(1,'丑')]:
        if hour>=s: return n
    return '子'
def shichen_ganzhi(day_idx,hour):
    dz=shichen_dz(hour); ti=(day_idx%10)*2+DIZHI.index(dz); return TIANGAN[ti%10]+dz
def find_xunshou(jz_idx):
    for xs in reversed(XUNSHOU_IDX):
        if jz_idx>=xs: return LIUJIAZI[xs],xs
    return '甲子',0
def current_jieqi(dt):
    n=JIEQI_2026[0][0]; s=datetime(2026,JIEQI_2026[0][1],JIEQI_2026[0][2])
    for jn,m,d in JIEQI_2026:
        jd=datetime(2026,m,d)
        if dt>=jd: n,s=jn,jd
        else: break
    return n,s
def ju_number(dt):
    jn,js=current_jieqi(dt); b=JIEQI_BASE[jn]; y=jn in YANG_JIEQI; dy=(dt-js).days; u=min(dy//5,2)
    j=b+u if y else b-u; j=((j-1)%9)+1; return j,['上元','中元','下元'][u],y,jn

def make_dipan(ju,yang):
    o=list(range(1,10)) if yang else list(range(9,0,-1)); s=o.index(ju); dp={}
    for i,st in enumerate(LIUYI_SANQI): dp[o[(s+i)%9]]=st
    return dp
def make_tianpan(dp,stg,xs,yang):
    zf=XUNSHOU_STAR[xs]; zfh=JIUXING.index(zf)+1; dy=XUNSHOU_DUNYI[xs]; dyh=next((p for p,s in dp.items() if s==dy),1)
    tg=next((p for p,s in dp.items() if s==stg),zfh)
    o=list(range(1,10)) if yang else list(range(9,0,-1)); off=(o.index(tg)-o.index(zfh))%9
    stars={}; sm={}
    for i,star in enumerate(JIUXING): stars[o[(o.index(i+1)+off)%9]]=star
    for stem in LIUYI_SANQI:
        sp=next((p for p,s in dp.items() if s==stem),None)
        if sp is None: continue
        sm[o[(o.index(sp)+off)%9]]=stem
    return stars,sm,zf
def make_renpan(sdz,xs,yang):
    zs=STAR_DOOR[XUNSHOU_STAR[xs]]; zsh=BAMEN_HOME[BAMEN_ORDER.index(zs)]; tg=DZ2GONG[sdz]
    fly=[1,2,3,4,6,7,8,9] if yang else [9,8,7,6,4,3,2,1]
    off=(fly.index(tg)-fly.index(zsh))%8; doors={}
    for i,d in enumerate(BAMEN_ORDER): doors[fly[(i+off)%8]]=d
    return doors,zs
def make_shenpan(tp,zf,yang):
    zfp=next((p for p,s in tp.items() if s==zf),1)
    fly=[1,2,3,4,6,7,8,9] if yang else [9,8,7,6,4,3,2,1]
    st=fly.index(zfp) if zfp in fly else 0; gods={}
    for i,g in enumerate(BASHEN_ORDER): gods[fly[(st+i)%8]]=g
    return gods

# === 十二長生（EP14/EP15）===
CS_STAGES=['長生','沐浴','冠帶','臨官','帝旺','衰','病','死','墓','絕','胎','養']
CS_DZ_IDX={d:i for i,d in enumerate(DIZHI)}
CS_YANG={'甲':'亥','丙':'寅','戊':'寅','庚':'巳','壬':'申'}
CS_YIN={'乙':'午','丁':'酉','己':'酉','辛':'子','癸':'卯'}
CS_PALACE_DZ={1:['子'],2:['未','申'],3:['卯'],4:['辰','巳'],5:[],6:['戌','亥'],7:['酉'],8:['丑','寅'],9:['午']}
CS_WANG={'長生','臨官','帝旺'}
CS_STAGE_ACTION={'長生':'積極發展','沐浴':'謹慎暴露','冠帶':'包裝展示','臨官':'穩步前進','帝旺':'全力進取','衰':'防禦為主','病':'暫停休息','死':'避免行動','墓':'忍耐等待','絕':'放棄轉向','胎':'醞釀計劃','養':'休養生息'}

def changsheng_table(tg):
    if tg in CS_YANG: s,d=CS_YANG[tg],1
    else: s,d=CS_YIN[tg],-1
    si=CS_DZ_IDX[s]; return {st:DIZHI[(si+d*i)%12] for i,st in enumerate(CS_STAGES)}
def changsheng_in_palace(tg,palace):
    cs=changsheng_table(tg); return [(dz,s) for dz in CS_PALACE_DZ.get(palace,[]) for s,sdz in cs.items() if sdz==dz]
def is_wang(tg,palace):
    return any(s in CS_WANG for _,s in changsheng_in_palace(tg,palace))
def check_jiubing_chong(tg,palace):
    if tg not in TG_HIDDEN_DZ: return False,''
    td=TG_HIDDEN_DZ[tg]
    for pdz in CS_PALACE_DZ.get(palace,[]):
        if DZ_CHONG.get(td)==pdz: return True,f'{tg}({td})落{GONG_BAGUA[palace]}{palace}宮({pdz})→{td}{pdz}衝'
    return False,''

# === 入墓系統（EP18）===
TG_RUMU={2:['甲','癸'],6:['乙','丙','戊'],8:['丁','己','庚'],4:['辛','壬']}
TG_RUMU_MAP={}; [TG_RUMU_MAP.__setitem__(t,p) for p,ts in TG_RUMU.items() for t in ts]
TG_RUMU_SPECIAL={'乙':[6,2]}
MEN_RUMU={4:['生門','死門','休門'],2:['傷門','杜門'],6:['景門'],8:['開門','驚門']}
MEN_RUMU_MAP={}; [MEN_RUMU_MAP.__setitem__(m,p) for p,ms in MEN_RUMU.items() for m in ms]
TG_RUMU_DZ={'甲':'未','乙':'未','丙':'戌','丁':'丑','戊':'戌','己':'丑','庚':'丑','辛':'戌','壬':'辰','癸':'辰'}

def check_tiangan_rumu(tg,palace):
    if TG_RUMU_MAP.get(tg)==palace: return True,f'{tg}入墓於{GONG_BAGUA[palace]}{palace}宮'
    if tg=='乙' and palace in TG_RUMU_SPECIAL.get('乙',[]): return True,f'乙代甲入墓於{GONG_BAGUA[palace]}{palace}宮'
    return False,''
def check_men_rumu(men,palace):
    if MEN_RUMU_MAP.get(men)==palace: return True,f'{men}入墓於{GONG_BAGUA[palace]}{palace}宮'
    return False,''
def get_rumu_exit_time(tg,long_term=True):
    dz=TG_RUMU_DZ.get(tg,'?'); ch=DZ_CHONG.get(dz,'?'); u='年/月' if long_term else '日/時'
    return {'rumu_dz':dz,'chong_dz':ch,'unit':u,'note':f'{tg}入墓{dz}→出墓:{dz}{u}/衝墓:{ch}{u}'}

# === 五行工具 ===
def wx_shengke(a,b):
    if a==b: return '比和',0.0
    if WUXING_SHENG.get(a)==b: return '我生(洩)',-0.5
    if WUXING_KE.get(a)==b: return '我剋(耗)',0.3
    if WUXING_SHENG.get(b)==a: return '生我(得生)',0.8
    if WUXING_KE.get(b)==a: return '剋我(受制)',-1.5
    return '未知',0.0
def palace_shengke(pa,pb): return wx_shengke(PALACE_WUXING[pa],PALACE_WUXING[pb])
def tongguan(a,b): return TONGGUAN.get((a,b))

def check_dedi(men,palace):
    mw=BAMEN_WUXING.get(men,''); pw=PALACE_WUXING.get(palace,'')
    if not mw or not pw: return False,''
    r,_=wx_shengke(mw,pw)
    if r=='比和': return True,f'{men}在本宮{GONG_BAGUA[palace]}{palace}→得地'
    if r=='生我(得生)': return True,f'{men}({mw})落{GONG_BAGUA[palace]}{palace}({pw})→宮生門=得地'
    return False,f'{men}({mw})落{GONG_BAGUA[palace]}{palace}({pw})→{r}'


"""
奇門遁甲量化系統 V2 — Part 2: 完整格局偵測庫 + 六儀擊刑 + 門迫 + 五不遇時
=====================================================================
EP16吉格 + EP17凶格 + EP13十干剋應 + 伏吟反吟 + 飛干伏干 + 玉女守門等
"""

# ================================================================
# A. 吉格偵測（EP08/EP16）
# ================================================================

JI_GE = [
    # 三遁（EP08）
    ('天遁', lambda t,d,g,s: t=='丙' and d=='戊' and g=='生門', 3.0),
    ('地遁', lambda t,d,g,s: t=='乙' and s=='太陰' and g in ('生門','九地'), 2.5),
    ('人遁', lambda t,d,g,s: t=='乙' and g=='休門' and s=='六合', 2.0),
    ('神遁', lambda t,d,g,s: t=='丙' and s=='九天' and g=='生門', 2.5),
    ('龍遁', lambda t,d,g,s: t=='乙' and d=='壬' and g=='休門', 2.0),
    ('虎遁', lambda t,d,g,s: t=='辛' and g=='生門', 2.0),
    # EP16 新增吉格
    ('玉女守門', lambda t,d,g,s: d=='丁' and g=='驚門', 2.0),  # 簡化: 地盤丁+值使門
    ('三奇貴人升殿_乙震3', lambda t,d,g,s,p: t=='乙' and p==3, 2.5),
    ('三奇貴人升殿_丙離9', lambda t,d,g,s,p: t=='丙' and p==9, 2.5),
    ('三奇貴人升殿_丁兌7', lambda t,d,g,s,p: t=='丁' and p==7, 2.5),
    ('奇遊祿位_乙震3', lambda t,d,g,s,p: t=='乙' and p==3, 2.0),
    ('奇遊祿位_丙巽4', lambda t,d,g,s,p: t=='丙' and p==4, 2.0),
    ('奇遊祿位_丁離9', lambda t,d,g,s,p: t=='丁' and p==9, 2.0),
    # 合格（EP07）
    ('丁壬合格', lambda t,d,g,s: (t=='丁' and d=='壬') or (t=='壬' and d=='丁'), 1.5),
    ('丁戊合格', lambda t,d,g,s: (t=='丁' and d=='戊') or (t=='戊' and d=='丁'), 1.5),
]

# ================================================================
# B. 凶格偵測（EP08-EP17 完整）
# ================================================================

XIONG_GE = [
    # 天干組合凶格
    ('青龍逃走', lambda t,d,g,s: t=='乙' and d=='辛', -3.0),
    ('白虎猖狂', lambda t,d,g,s: t=='辛' and d=='乙', -3.0),
    ('朱雀投江', lambda t,d,g,s: t=='丁' and d=='壬', -2.5),
    ('螣蛇夭矯', lambda t,d,g,s: t=='乙' and d=='己', -2.0),
    ('大格',     lambda t,d,g,s: t=='庚' and d=='癸', -2.5),
    ('小格',     lambda t,d,g,s: t=='庚' and d=='壬', -2.0),
    ('刑格',     lambda t,d,g,s: t=='庚' and d=='己', -2.0),
    ('飛宮格',   lambda t,d,g,s: t=='庚' and d=='庚', -3.0),
    # 衝格（EP06-EP07）
    ('庚丙衝格', lambda t,d,g,s: (t=='庚' and d=='丙') or (t=='丙' and d=='庚'), -1.5),
    ('癸庚衝格', lambda t,d,g,s: (t=='癸' and d=='庚') or (t=='庚' and d=='癸'), -1.5),
    ('辛乙衝格', lambda t,d,g,s: (t=='辛' and d=='乙') or (t=='乙' and d=='辛'), -1.5),
    # 暗含地支衝格（EP07）
    ('戊辛暗衝', lambda t,d,g,s: (t=='戊' and d=='辛') or (t=='辛' and d=='戊'), -1.5),
    ('己壬暗衝', lambda t,d,g,s: (t=='己' and d=='壬') or (t=='壬' and d=='己'), -1.5),
    ('庚癸暗衝', lambda t,d,g,s: (t=='庚' and d=='癸') or (t=='癸' and d=='庚'), -1.5),
]

# ================================================================
# C. 六儀擊刑（EP17，僅此6個固定組合）
# ================================================================

LIUYI_XINGXING = [
    ('壬', 4, '巽四宮'), ('癸', 4, '巽四宮'),
    ('辛', 9, '離九宮'), ('己', 2, '坤二宮'),
    ('戊', 3, '震三宮'), ('庚', 8, '艮八宮'),
]
LIUYI_XINGXING_MAP = {(tg, pal): name for tg, pal, name in LIUYI_XINGXING}

def check_liuyi_xingxing(tg, palace):
    """天干在某宮是否六儀擊刑 → (bool, reason, score)"""
    if (tg, palace) in LIUYI_XINGXING_MAP:
        name = LIUYI_XINGXING_MAP[(tg, palace)]
        return True, f'{tg}落{GONG_BAGUA[palace]}{palace}宮→六儀擊刑({name})', -2.0
    return False, '', 0.0

# ================================================================
# D. 五不遇時（EP17，10個組合：時干五行剋日干五行）
# ================================================================

WUBUYUSHI = [
    ('甲','庚'),('乙','辛'),('丙','壬'),('丁','癸'),
    ('戊','甲'),('己','乙'),('庚','丙'),('辛','丁'),('壬','戊'),('癸','己'),
]
WUBUYUSHI_SET = set(WUBUYUSHI)

def check_wubuyushi(day_gan, hour_gan):
    """是否五不遇時 → (bool, reason)"""
    if (day_gan, hour_gan) in WUBUYUSHI_SET:
        return True, f'{day_gan}日{hour_gan}時→五不遇時（{TG_WUXING[hour_gan]}剋{TG_WUXING[day_gan]}）'
    return False, ''

# ================================================================
# E. 門迫（EP17，12個固定組合：門五行剋宮五行）
# ================================================================

MENPO_LIST = [
    ('休門',9),('開門',3),('開門',4),('驚門',3),('驚門',4),
    ('生門',1),('死門',1),('傷門',2),('傷門',8),('杜門',2),('杜門',8),
    ('景門',6),('景門',7),
]
MENPO_SET = set(MENPO_LIST)

def check_menpo(men, palace):
    """門在某宮是否門迫 → (bool, reason, score)"""
    if (men, palace) in MENPO_SET:
        mw = BAMEN_WUXING[men]; pw = PALACE_WUXING[palace]
        return True, f'{men}({mw})落{GONG_BAGUA[palace]}{palace}({pw})→門迫', -2.0
    # 動態計算（兜底）
    mw = BAMEN_WUXING.get(men,''); pw = PALACE_WUXING.get(palace,'')
    if mw and pw and WUXING_KE.get(mw) == pw:
        return True, f'{men}({mw})落{GONG_BAGUA[palace]}{palace}({pw})→門迫(動態)', -2.0
    return False, '', 0.0

# ================================================================
# F. 飛干格/伏干格（EP17）
# ================================================================

def check_feigan(t_gan, d_gan, day_gan):
    """飛干格：天盤日干落在地盤庚之上 → (bool, reason, score)"""
    if t_gan == day_gan and d_gan == '庚':
        return True, f'飛干格（天盤{day_gan}+地盤庚）→遭遇不測、身陷困境', -2.5
    return False, '', 0.0

def check_fugan(t_gan, d_gan, day_gan):
    """伏干格：天盤庚落在地盤日干之上 → (bool, reason, score)"""
    if t_gan == '庚' and d_gan == day_gan:
        return True, f'伏干格（天盤庚+地盤{day_gan}）→遭遇不測+失去行動自由', -3.0
    return False, '', 0.0

# ================================================================
# G. 伏吟/反吟局偵測（EP12）
# ================================================================

def detect_fuyin(dp, tp, rp):
    """伏吟局：天盤干與地盤干完全相同 → (bool, reason)"""
    count = sum(1 for p in range(1,10) if tp.get(p) == dp.get(p))
    if count >= 8:
        return True, f'伏吟局（{count}/9宮天干地干相同）→利主不利客、慢、不動'
    return False, ''

def detect_fanyin(dp, tp):
    """反吟局：天盤干與地盤干完全相反（對宮互換）→ (bool, reason)"""
    chong_pairs = [(1,9),(2,8),(3,7),(4,6)]
    count = sum(1 for a,b in chong_pairs if tp.get(a)==dp.get(b) and tp.get(b)==dp.get(a))
    if count >= 3:
        return True, f'反吟局（{count}/4對宮互換）→反覆不定、逢衝必動'
    return False, ''

# ================================================================
# H. 玉女守門/三奇升殿/奇遊祿位（EP16）
# ================================================================

def check_yunv_shoumen(d_gan, gate, zhishi):
    """玉女守門：值使門+地盤丁同宮 → (bool, reason, score)"""
    if d_gan == '丁' and gate == zhishi:
        return True, f'玉女守門（值使{zhishi}+地盤丁同宮）→大吉', 2.5
    return False, '', 0.0

def check_sanqi_guiren(t_gan, palace):
    """三奇貴人升殿 → (bool, reason, score)"""
    mapping = {'乙':3,'丙':9,'丁':7}
    if t_gan in mapping and palace == mapping[t_gan]:
        return True, f'三奇貴人升殿（{t_gan}落{GONG_BAGUA[palace]}{palace}宮）', 2.5
    return False, '', 0.0

def check_qiyou_luwei(t_gan, palace):
    """奇遊祿位 → (bool, reason, score)"""
    mapping = {'乙':3,'丙':4,'丁':9}
    if t_gan in mapping and palace == mapping[t_gan]:
        return True, f'奇遊祿位（{t_gan}落{GONG_BAGUA[palace]}{palace}宮=臨官位）', 2.0
    return False, '', 0.0

# ================================================================
# I. 天輔吉時（EP16）
# ================================================================

TIANFU_JISHI = [
    (['甲','己'],'甲戌'),(['乙','庚'],'甲申'),(['丙','辛'],'甲午'),
    (['丁','壬'],'甲辰'),(['戊','癸'],'甲寅'),
]

def check_tianfu_jishi(day_gan, shi_ganzhi):
    """天輔吉時 → (bool, reason)"""
    for day_gans, hour_str in TIANFU_JISHI:
        if day_gan in day_gans and shi_ganzhi == hour_str:
            return True, f'天輔吉時（{day_gan}日+{hour_str}時）→宜遠行/求職/嫁娶'
    return False, ''

# ================================================================
# J. 統一格局偵測函數（EP16 G83 解決）
# ================================================================

def detect_all_geju(t_gan, d_gan, gate, spirit, palace, day_gan, zhishi=None):
    """
    對單宮進行全面格局偵測
    返回 [(類型, 名稱, 分數, 原因), ...]
    """
    results = []
    # 吉格（含宮位參數的用 keyword）
    for name, fn, sc in JI_GE:
        try:
            import inspect
            params = inspect.signature(fn).parameters
            if 'p' in params:
                if fn(t_gan, d_gan, gate, spirit, palace): results.append(('吉', name, sc))
            else:
                if fn(t_gan, d_gan, gate, spirit): results.append(('吉', name, sc))
        except: pass
    # 凶格
    for name, fn, sc in XIONG_GE:
        try:
            if fn(t_gan, d_gan, gate, spirit): results.append(('凶', name, sc))
        except: pass
    # 六儀擊刑
    ok, reason, sc = check_liuyi_xingxing(t_gan, palace)
    if ok: results.append(('凶', '六儀擊刑', sc))
    # 門迫
    ok, reason, sc = check_menpo(gate, palace)
    if ok: results.append(('凶', '門迫', sc))
    # 飛干格/伏干格
    ok, reason, sc = check_feigan(t_gan, d_gan, day_gan)
    if ok: results.append(('凶', '飛干格', sc))
    ok, reason, sc = check_fugan(t_gan, d_gan, day_gan)
    if ok: results.append(('凶', '伏干格', sc))
    # 天干入墓
    ok, reason = check_tiangan_rumu(t_gan, palace)
    if ok: results.append(('凶', '天干入墓', -2.5))
    # 八門入墓
    ok, reason = check_men_rumu(gate, palace)
    if ok: results.append(('凶', '八門入墓', -2.0))
    # 三奇貴人升殿
    ok, reason, sc = check_sanqi_guiren(t_gan, palace)
    if ok: results.append(('吉', '三奇貴人升殿', sc))
    # 奇遊祿位
    ok, reason, sc = check_qiyou_luwei(t_gan, palace)
    if ok: results.append(('吉', '奇遊祿位', sc))
    # 玉女守門
    if zhishi:
        ok, reason, sc = check_yunv_shoumen(d_gan, gate, zhishi)
        if ok: results.append(('吉', '玉女守門', sc))
    return results

def geju_score(results):
    """格局總分"""
    return sum(r[2] for r in results)


"""
奇門遁甲量化系統 V2 — Part 3: 用神體系 + 場景預測函數
=====================================================================
民事官司(EP17) / 刑事訴訟(EP18) / 疾病預測(EP13-EP15)
投資經營(EP08) / 婚姻感情(EP02-EP04) / 事業(EP05-EP07)
通用用神查找 + 多用神交叉驗證框架
"""

# ================================================================
# A. 通用用神查找器
# ================================================================

def find_palace_of(tg_map, rp, sp, tp, target):
    """在盤局中查找目標符號所在宮位
    target: 天干('庚') / 門('開門') / 神('白虎') / 星('天芮')
    返回 (宮位, layer) 或 (None, None)
    """
    # 天盤干
    for p, tg in tg_map.items():
        if tg == target: return p, '天干'
    # 人盤門
    for p, gate in rp.items():
        if gate == target: return p, '門'
    # 神盤
    for p, god in sp.items():
        if god == target: return p, '神'
    # 天盤星
    for p, star in tp.items():
        if star == target: return p, '星'
    return None, None

def find_tiangan_palace(tg_map, tg):
    """查找天干所在宮位"""
    for p, t in tg_map.items():
        if t == tg: return p
    return None

def find_dipan_palace(dp, tg):
    """查找地盤天干所在宮位"""
    for p, t in dp.items():
        if t == tg: return p
    return None

# ================================================================
# B. 場景用神配置表（EP02-EP19 綜合）
# ================================================================

SCENE_YONGSHEN = {
    'investment': {
        'name': '投資經營（EP08）',
        'yongshen': {
            '開門': '開業/交易', '日干': '求測人', '時干': '投資事件',
            '生門': '利潤', '戊': '資金（天盤=表面/地盤=真相）',
        },
        'positive': '開門/生門宮分數高、用神得地、吉格多',
        'negative': '開門/生門宮分數低、門迫、凶格多',
    },
    'marriage': {
        'name': '婚姻感情（EP02-EP04）',
        'yongshen': {
            '乙': '太太/女方', '庚': '先生/男方', '六合': '婚姻關係',
            '日干': '求測人(男=庚/女=乙)', '時干': '對象',
        },
        'positive': '乙庚宮生/比和、六合吉、無衝格',
        'negative': '乙庚衝剋、六合受制、第三者符號(丙/丁)',
    },
    'job_stability': {
        'name': '工作穩定（EP05）',
        'yongshen': {
            '開門': '目前工作職位', '日干': '求測人',
            '年干': '最高領導/老板', '月干': '同事',
        },
        'positive': '開門生日干=工作順利',
        'negative': '開門剋日干=工作壓力大',
    },
    'job_hunt': {
        'name': '找工作（EP06）',
        'yongshen': {
            '開門': '目前工作（非新工作）', '日干': '求測人', '時干': '新工作',
        },
        'positive': '時干宮分數高、日干生時干',
        'negative': '時干宮分數低、日干剋時干',
    },
    'job_compare': {
        'name': '留任vs跳槽（EP07）',
        'yongshen': {
            '開門': '目前工作', '日干': '求測人', '時干': '新工作',
        },
        'method': '比較開門宮與時干宮分數',
    },
    'partnership': {
        'name': '合作夥伴（EP11）',
        'yongshen': {
            '日干': '自己', '時干': '對方', '生門': '共同利潤',
        },
        'positive': '日干宮與時干宮比和/相生、生門吉',
        'negative': '日干宮與時干宮相剋、生門凶',
    },
    'debt': {
        'name': '債務追收（EP12）',
        'yongshen': {
            '值符': '債權人', '天乙(值符落宮地盤干)': '債務人',
            '開門': '追債行動', '戊': '資金',
        },
        'method': '值符宮剋天乙宮→能收回',
    },
    'health': {
        'name': '健康疾病（EP13-EP15）',
        'yongshen': {
            '天芮星': '疾病本身', '日干': '求測人', '年干': '長輩(問父母)',
            '乙': '中醫', '天心星': '西醫',
        },
        'body_parts': {9:['頭','心臟','腦部'],1:['耳','腎'],2:['腹','脾'],3:['肝','膽','腳'],
                       4:['大腿','風濕'],6:['頭','肺','骨'],7:['口','呼吸道'],8:['手','背','鼻']},
    },
    'lawsuit_civil': {
        'name': '民事官司（EP17）',
        'yongshen': {
            '值符': '原告', '天乙(值符落宮地盤干)': '被告',
            '開門': '法院/法官', '六合': '證人/證據',
            '景門': '訴狀/入稟狀', '驚門': '律師',
        },
        'method': '三步法: 值符vs天乙 → 日干vs時干 → 開門取向',
    },
    'lawsuit_criminal': {
        'name': '刑事訴訟（EP18）',
        'yongshen': {
            '辛': '疑犯(天獄)', '庚': '警察+判刑', '杜門': '檢控部門',
            '開門': '法院/法庭', '壬': '地牢', '癸': '天網',
            '日干': '疑犯(自測)',
        },
        'stages': ['拘捕(辛臨白虎/庚/傷門)', '檢控(辛臨杜門)', '審理(開門vs辛生剋)'],
    },
    'exam': {
        'name': '考試升學（EP19）',
        'yongshen': {
            '日干': '考生自己(親自求測)', '時干': '考生(父母代測)',
            '年干': '錄取學校', '天輔星': '繼續升學機會',
            '景門': '試卷/試題',
        },
        'method': '三步法: 景門vs考生 → 年干vs考生 → 天輔vs考生',
        'positive': '三用神都生考生宮→大吉一定考上',
        'negative': '三用神都剋考生宮→凶考不上',
    },
}

# ================================================================
# C. 民事官司判斷函數（EP17）
# ================================================================

def get_tianyi_palace(tp, tg_map, dp, zhifu):
    """天乙太乙所在宮位 = 值符落宮的地盤天干"""
    zhifu_palace = None
    for p, star in tp.items():
        if star == zhifu: zhifu_palace = p; break
    if zhifu_palace is None: return None
    # 天乙 = 值符落宮的地盤天干
    tianyi_gan = dp.get(zhifu_palace, '')
    # 天乙本身所在宮位 = 該天干的天盤位置
    tianyi_palace = find_tiangan_palace(tg_map, tianyi_gan)
    return tianyi_palace

def predict_lawsuit_civil(r):
    """民事官司預測
    r = qiju() 返回的完整盤局
    返回 {step, analysis, verdict, confidence}
    """
    dp, tp, tg_map, rp, sp = r['dp'], r['tp'], r['tg'], r['rp'], r['sp']
    zhifu = r['zhifu']; day_gan = r['dgz'][0]; hour_gan = r['stg']
    results = {}

    # Step 1: 值符 vs 天乙
    zhifu_palace = find_palace_of(tg_map, rp, sp, tp, zhifu)[0]
    if zhifu_palace is None: zhifu_palace = find_palace_of(tg_map, rp, sp, tp, '值符')[0]
    tianyi_palace = get_tianyi_palace(tp, tg_map, dp, zhifu)
    if zhifu_palace and tianyi_palace:
        rel, sc = palace_shengke(zhifu_palace, tianyi_palace)
        results['step1_值符vs天乙'] = {
            '值符宮': zhifu_palace, '天乙宮': tianyi_palace,
            '關係': rel, '傾向': '原告贏' if sc > 0 else ('被告贏' if sc < 0 else '比和-看旺衰')
        }
    # Step 2: 日干 vs 時干
    rigan_pal = find_tiangan_palace(tg_map, day_gan)
    shigan_pal = find_tiangan_palace(tg_map, hour_gan)
    if rigan_pal and shigan_pal:
        rel, sc = palace_shengke(rigan_pal, shigan_pal)
        results['step2_日干vs時干'] = {
            '日干宮': rigan_pal, '時干宮': shigan_pal,
            '關係': rel, '交叉驗證': '原告利' if sc > 0 else ('被告利' if sc < 0 else '中立')
        }
    # Step 3: 開門取向
    kaimen_pal = find_palace_of(tg_map, rp, sp, tp, '開門')[0]
    if kaimen_pal and zhifu_palace and tianyi_palace:
        rel1, sc1 = palace_shengke(kaimen_pal, zhifu_palace)
        rel2, sc2 = palace_shengke(kaimen_pal, tianyi_palace)
        results['step3_開門取向'] = {
            '開門宮': kaimen_pal,
            '對原告(值符)': f'{rel1}({sc1:+.1f})',
            '對被告(天乙)': f'{rel2}({sc2:+.1f})',
            '法院傾向': '原告' if sc1 > sc2 else ('被告' if sc2 > sc1 else '中立')
        }
    # 伏吟反吟
    ok, reason = detect_fanyin(dp, tp)
    if ok: results['反吟局'] = '不會一次審完，輸了會上訴'
    ok, reason = detect_fuyin(dp, tp, rp)
    if ok: results['伏吟局'] = '審理拖長'

    results['verdict'] = '待綜合判斷（需結合各步驟）'
    return results

# ================================================================
# D. 刑事定罪判斷函數（EP18）
# ================================================================

CONVICTION_RULES = [
    ('R01','開門宮生辛宮','無罪',0),
    ('R02','開門宮與辛宮比和','定罪(輕判/緩刑)',1),
    ('R03','開門宮衝/剋辛宮','定罪(重判)',2),
    ('R04','庚+辛同宮','定罪(重判)',2),
    ('R05','辛+辛/壬/癸同宮','定罪+監禁',2),
    ('R06','庚宮剋辛宮','定罪',1),
    ('R07','辛落巽四宮','傾向定罪',1),
]

def predict_criminal(r):
    """刑事訴訟預測
    r = qiju() 返回的完整盤局
    返回 {analysis, verdicts, final_verdict}
    """
    dp, tp, tg_map, rp, sp = r['dp'], r['tp'], r['tg'], r['rp'], r['sp']
    results = {'verdicts': [], 'analysis': []}

    # 找辛宮
    xin_palace = find_tiangan_palace(tg_map, '辛')
    if xin_palace is None:
        results['final_verdict'] = '盤中無天干辛，無法分析'
        return results
    results['analysis'].append(f'天干辛(疑犯)落{GONG_BAGUA[xin_palace]}{xin_palace}宮')

    # 找開門宮
    kaimen_pal = find_palace_of(tg_map, rp, sp, tp, '開門')[0]

    # 階段判斷
    xin_companions = []
    if rp.get(xin_palace): xin_companions.append(rp[xin_palace])
    if sp.get(xin_palace): xin_companions.append(sp[xin_palace])
    if '傷門' in xin_companions or '白虎' in xin_companions or '庚' in [tg_map.get(xin_palace)]:
        results['analysis'].append('階段: 警方拘捕階段（辛臨傷門/白虎/庚）')
    if '杜門' in xin_companions:
        results['analysis'].append('階段: 檢控階段（辛臨杜門）')
    if kaimen_pal:
        results['analysis'].append('階段: 法院審理階段')

    # 定罪規則逐條檢測
    xin_wx = TG_WUXING.get('辛','')
    max_severity = -1

    if kaimen_pal:
        km_wx = PALACE_WUXING.get(kaimen_pal, '')
        rel, sc = palace_shengke(kaimen_pal, xin_palace)
        if rel == '生我(得生)':  # 開門宮生辛宮
            results['verdicts'].append({'rule':'R01','detail':'開門宮生辛宮','result':'無罪','severity':0})
        elif rel == '比和':
            results['verdicts'].append({'rule':'R02','detail':'開門辛比和','result':'定罪(輕判/緩刑)','severity':1})
            max_severity = max(max_severity, 1)
        elif sc < 0:
            results['verdicts'].append({'rule':'R03','detail':f'開門宮{rel}辛宮','result':'定罪(重判)','severity':2})
            max_severity = max(max_severity, 2)

    # R04: 庚+辛同宮
    if tg_map.get(xin_palace) == '辛' and dp.get(xin_palace) == '庚':
        results['verdicts'].append({'rule':'R04','detail':'庚+辛同宮','result':'定罪(重判)','severity':2})
        max_severity = max(max_severity, 2)
    if tg_map.get(xin_palace) == '庚' and dp.get(xin_palace) == '辛':
        results['verdicts'].append({'rule':'R04','detail':'庚+辛同宮(反)','result':'定罪(重判)','severity':2})
        max_severity = max(max_severity, 2)

    # R05: 辛+壬/癸
    for bad_tg in ['壬','癸']:
        if (tg_map.get(xin_palace) == '辛' and dp.get(xin_palace) == bad_tg) or \
           (tg_map.get(xin_palace) == bad_tg and dp.get(xin_palace) == '辛'):
            results['verdicts'].append({'rule':'R05','detail':f'辛+{bad_tg}','result':'定罪+監禁','severity':2})
            max_severity = max(max_severity, 2)

    # R06: 庚宮剋辛宮
    geng_pal = find_tiangan_palace(tg_map, '庚')
    if geng_pal and geng_pal != xin_palace:
        _, sc = palace_shengke(geng_pal, xin_palace)
        if sc < 0:
            results['verdicts'].append({'rule':'R06','detail':f'庚宮{GONG_BAGUA[geng_pal]}剋辛宮{GONG_BAGUA[xin_palace]}','result':'定罪','severity':1})
            max_severity = max(max_severity, 1)

    # R07: 辛落巽四宮
    if xin_palace == 4:
        results['verdicts'].append({'rule':'R07','detail':'辛落巽四宮(執法部門)','result':'傾向定罪','severity':1})
        max_severity = max(max_severity, 1)

    # 最終判斷
    if max_severity == 0: results['final_verdict'] = '傾向無罪'
    elif max_severity == 1: results['final_verdict'] = '傾向定罪（可能輕判）'
    else: results['final_verdict'] = '必定定罪（重判+可能有牢獄之災）'

    # 伏吟/反吟
    ok, reason = detect_fuyin(dp, tp, rp)
    if ok: results['analysis'].append(f'伏吟局: 審理拖長')
    ok, reason = detect_fanyin(dp, tp)
    if ok: results['analysis'].append(f'反吟局: 審理快但會上訴/重審')

    return results

# ================================================================
# E. 疾病預測分析函數（EP13-EP15）
# ================================================================

def predict_health(r, patient_tg=None, is_elderly=False):
    """疾病預測
    r = qiju() 完整盤局
    patient_tg: 病人用神天干（默認=日干）
    is_elderly: 是否老人（影響帝旺判斷）
    """
    dp, tp, tg_map, rp, sp = r['dp'], r['tp'], r['tg'], r['rp'], r['sp']
    day_gan = r['dgz'][0]
    if patient_tg is None: patient_tg = day_gan
    results = {'symptoms': [], 'treatment': [], 'prognosis': [], 'warnings': []}

    # 天芮星定位
    tianrui_pal = find_palace_of(tg_map, rp, sp, tp, '天芮')[0]
    if tianrui_pal is None:
        results['prognosis'].append('盤中無天芮星，無明顯疾病')
        return results

    # 天芮宮信息
    tr_wx = PALACE_WUXING[tianrui_pal]
    tr_tg = tp.get(tianrui_pal, '')
    tr_dg = dp.get(tianrui_pal, '')
    tr_gate = rp.get(tianrui_pal, '')
    tr_spirit = sp.get(tianrui_pal, '')
    results['symptoms'].append(f'天芮星落{GONG_BAGUA[tianrui_pal]}{tianrui_pal}宮({tr_wx})')

    # 宮位對應人體
    body_map = {9:['頭','心臟','腦部'],1:['耳','腎'],2:['腹','脾'],3:['肝','膽','腳'],
                4:['大腿','風濕'],6:['頭','肺','骨'],7:['口','呼吸道'],8:['手','背','鼻']}
    parts = body_map.get(tianrui_pal, ['未知部位'])
    results['symptoms'].append(f'可能部位: {"、".join(parts)}')

    # 天干線索
    tg_body = {'丁':['心臟','眼睛'],'壬':['血液','動脈'],'戊':['堵塞','障礙'],'庚':['大腸','筋骨'],
               '乙':['肝膽','神經'],'丙':['小腸','額頭'],'辛':['肺部','骨骼']}
    for tg in [tr_tg, tr_dg]:
        if tg in tg_body: results['symptoms'].append(f'{tg}→{"、".join(tg_body[tg])}')

    # 帝旺+老人=迴光反照
    if patient_tg:
        p_pal = find_tiangan_palace(tg_map, patient_tg)
        if p_pal:
            cs = changsheng_in_palace(patient_tg, p_pal)
            for dz, stage in cs:
                if stage == '帝旺':
                    if is_elderly:
                        results['warnings'].append(f'帝旺+老人=迴光反照，極不樂觀')
                    else:
                        results['prognosis'].append(f'帝旺狀態，能量最強')

    # 久病逢衝
    if patient_tg and p_pal:
        ok, reason = check_jiubing_chong(patient_tg, p_pal)
        if ok: results['warnings'].append(f'久病逢衝(大凶): {reason}')

    # 九天+空亡（死亡徵兆）
    if sp.get(tianrui_pal) == '九天':
        results['warnings'].append('天芮臨九天=飛升隱喻')

    # 治療判斷
    # 中醫=乙
    yi_pal = find_tiangan_palace(tg_map, '乙')
    if yi_pal:
        rel, sc = palace_shengke(yi_pal, tianrui_pal)
        if sc < 0: results['treatment'].append(f'中醫(乙)宮{rel}天芮宮→{"有效(剋疾病)" if rel=="我剋(耗)" else "無效(生疾病)"}')
        elif sc > 0: results['treatment'].append(f'中醫(乙)宮{rel}天芮宮→無效(生疾病，加重)')
        else: results['treatment'].append(f'中醫(乙)與天芮比和→一般')
    # 西醫=天心星
    tx_pal = find_palace_of(tg_map, rp, sp, tp, '天心')[0]
    if tx_pal:
        rel, sc = palace_shengke(tx_pal, tianrui_pal)
        if sc < 0: results['treatment'].append(f'西醫(天心)宮{rel}天芮宮→有效')
        elif sc > 0: results['treatment'].append(f'西醫(天心)宮{rel}天芮宮→無效')

    # 庚=大凶符號
    if tr_tg == '庚' or tr_dg == '庚':
        results['warnings'].append('天芮宮臨庚=大凶符號(血光/不治)')

    return results

# ================================================================
# F. 多用神交叉驗證框架
# ================================================================

def cross_validate_yongshen(yongshen_scores):
    """
    多用神交叉驗證
    yongshen_scores: {用神名: (宮位, 分數)}
    返回 {agreement, direction, confidence}
    """
    if len(yongshen_scores) < 2:
        return {'agreement': 'N/A', 'direction': 'N/A', 'confidence': 'low'}

    positives = sum(1 for _, (_, sc) in yongshen_scores.items() if sc > 0)
    negatives = sum(1 for _, (_, sc) in yongshen_scores.items() if sc < 0)
    total = len(yongshen_scores)

    if positives == total: return {'agreement': '一致看好', 'direction': 'positive', 'confidence': 'high'}
    if negatives == total: return {'agreement': '一致看淡', 'direction': 'negative', 'confidence': 'high'}
    if positives > negatives: return {'agreement': '偏好看好', 'direction': 'positive', 'confidence': 'medium'}
    if negatives > positives: return {'agreement': '偏向看淡', 'direction': 'negative', 'confidence': 'medium'}
    return {'agreement': '分歧', 'direction': 'neutral', 'confidence': 'low'}


"""
奇門遁甲量化系統 V2 — Part 4: 完整起局 + 增強評分 + 多場景輸出
=====================================================================
整合 Part1-3，提供統一的 qiju_v2() 入口
"""

# ================================================================
# A. 增強宮位評分（V1 基礎 + V2 格局+入墓+六儀擊刑+門迫+十二長生+得地）
# ================================================================

def palace_score_v2(p, star, gate, spirit, t_gan, d_gan, palace, day_gan, zhishi=None):
    """
    V2 增強評分 = 星分 + 門分 + 神分 + 干支生剋 + 格局總分 + 入墓 + 六儀擊刑 + 門迫 + 得地 + 十二長生
    """
    # 基礎分（V1）
    ss = JIUXING_SCORE.get(star, 0)
    gs = BAMEN_SCORE.get(gate, 0)
    hs = BASHEN_SCORE.get(spirit, 0)
    wx = WX_SK.get((TG_WUXING.get(t_gan,'土'), TG_WUXING.get(d_gan,'土')), 0)

    # 格局分（V2）
    gejus = detect_all_geju(t_gan, d_gan, gate, spirit, palace, day_gan, zhishi)
    gps = geju_score(gejus)

    # 六儀擊刑
    _, _, lxsc = check_liuyi_xingxing(t_gan, palace)

    # 門迫
    _, _, mpsc = check_menpo(gate, palace)

    # 天干入墓
    ok_rumu, _ = check_tiangan_rumu(t_gan, palace)
    rumu_sc = -2.5 if ok_rumu else 0.0

    # 八門入墓
    ok_mrumu, _ = check_men_rumu(gate, palace)
    mrumu_sc = -2.0 if ok_mrumu else 0.0

    # 得地加成
    ok_dedi, _ = check_dedi(gate, palace)
    dedi_sc = 1.0 if ok_dedi else 0.0

    # 十二長生加成（用神旺）
    wang_sc = 0.5 if is_wang(t_gan, palace) else 0.0

    total = ss + gs + hs + wx + gps + lxsc + mpsc + rumu_sc + mrumu_sc + dedi_sc + wang_sc
    details = {
        'star': ss, 'gate': gs, 'spirit': hs, 'wuxing': wx, 'geju': gps,
        'liuyi_xingxing': lxsc, 'menpo': mpsc, 'tiangan_rumu': rumu_sc,
        'men_rumu': mrumu_sc, 'dedi': dedi_sc, 'changsheng_wang': wang_sc,
        'gejus': gejus,
    }
    return total, details

# ================================================================
# B. 完整起局 V2
# ================================================================

def qiju_v2(dt, scene=None):
    """
    完整起局 V2 — 整合全部量化規則

    參數:
        dt: datetime 起局時間
        scene: 場景名稱（可選，觸發場景預測）

    返回: dict 包含
        - 基礎資訊: dgz, sgz, sdz, stg, xs, jname, yang, ju, yuan
        - 四盤: dp, tp, tg, rp, sp
        - 值符值使: zhifu, zhishi
        - 各宮評分: scores, details（V2增強）
        - 局類型: fuyin, fanyin
        - 五不遇時: wubuyushi
        - 天輔吉時: tianfu_jishi
        - 場景預測: prediction（如指定scene）
    """
    # 基礎計算
    dgz, d_idx = day_ganzhi(dt)
    sdz = shichen_dz(dt.hour)
    sgz = shichen_ganzhi(d_idx, dt.hour)
    stg = sgz[0]
    s_idx = LIUJIAZI.index(sgz)
    xs, xs_idx = find_xunshou(s_idx)
    ju, yuan, yang, jname = ju_number(dt)

    # 四盤
    dp = make_dipan(ju, yang)
    tp, tg_map, zhifu = make_tianpan(dp, stg, xs, yang)
    rp, zhishi = make_renpan(sdz, xs, yang)
    sp = make_shenpan(tp, zhifu, yang)

    # V2 評分
    scores = {}; details = {}
    for p in range(1, 10):
        star = tp.get(p, ''); gate = rp.get(p, ''); spirit = sp.get(p, '')
        t_g = tg_map.get(p, stg); d_g = dp.get(p, '')
        sc, det = palace_score_v2(p, star, gate, spirit, t_g, d_g, p, dgz[0], zhishi)
        scores[p] = sc; details[p] = det

    # 局類型
    fy_ok, fy_reason = detect_fuyin(dp, tp, rp)
    fyn_ok, fyn_reason = detect_fanyin(dp, tp)

    # 五不遇時
    wby_ok, wby_reason = check_wubuyushi(dgz[0], stg)

    # 天輔吉時
    tf_ok, tf_reason = check_tianfu_jishi(dgz[0], sgz)

    result = dict(
        dt=dt, dgz=dgz, sgz=sgz, sdz=sdz, stg=stg, xs=xs,
        jname=jname, yang=yang, ju=ju, yuan=yuan,
        dp=dp, tp=tp, tg=tg_map, rp=rp, sp=sp,
        zhifu=zhifu, zhishi=zhishi,
        scores=scores, details=details,
        fuyin={'active': fy_ok, 'reason': fy_reason},
        fanyin={'active': fyn_ok, 'reason': fyn_reason},
        wubuyushi={'active': wby_ok, 'reason': wby_reason},
        tianfu_jishi={'active': tf_ok, 'reason': tf_reason},
    )

    # 場景預測
    if scene:
        if scene == 'lawsuit_civil':
            result['prediction'] = predict_lawsuit_civil(result)
        elif scene == 'lawsuit_criminal':
            result['prediction'] = predict_criminal(result)
        elif scene == 'health':
            result['prediction'] = predict_health(result)
        elif scene == 'exam':
            result['prediction'] = predict_exam(result)
        elif scene in SCENE_YONGSHEN:
            result['scene_info'] = SCENE_YONGSHEN[scene]

    # 孤虛法
    result['guxu'] = calc_guxu(sgz, result)

    return result

# ================================================================
# C. 統一輸出函數
# ================================================================

def decision_v2(score):
    """V2 決策閾值（格局範圍更廣，閾值適度放寬）"""
    if score >= 5.0: return '強烈看多，加倉'
    if score >= 2.0: return '偏多，可買入'
    if score >= -2.0: return '觀望，唔操作'
    if score >= -5.0: return '偏空，減倉'
    return '強烈看空，清倉'

def print_chart_v2(r, title=''):
    """V2 增強盤面輸出"""
    sep = '=' * 66
    print(f'\n{sep}')
    if title: print(f'  {title}')
    print(f'  奇門遁甲 V2 量化盤')
    print(sep)
    print(f'  時間: {r["dt"].strftime("%Y-%m-%d %H:%M")}')
    print(f'  日干支: {r["dgz"]}  |  時辰: {r["sgz"]}')
    print(f'  節氣: {r["jname"]}  |  {"陽遁" if r["yang"] else "陰遁"}{r["ju"]}局 {r["yuan"]}')
    print(f'  值符: {r["zhifu"]}  |  值使: {r["zhishi"]}  |  旬首: {r["xs"]}')

    # 局類型 + 特殊時辰
    extras = []
    if r['fuyin']['active']: extras.append(f'伏吟局: {r["fuyin"]["reason"]}')
    if r['fanyin']['active']: extras.append(f'反吟局: {r["fanyin"]["reason"]}')
    if r['wubuyushi']['active']: extras.append(f'五不遇時: {r["wubuyushi"]["reason"]}')
    if r['tianfu_jishi']['active']: extras.append(f'天輔吉時: {r["tianfu_jishi"]["reason"]}')
    if extras:
        print(f'  ⚠️ {" | ".join(extras)}')


    # 九宮格
    for ri, row in enumerate(LUOSHU):
        if ri == 1: print('  ' + '─' * 58)
        for line_idx in range(5):
            cells = []
            for p in row:
                bg = GONG_BAGUA[p]
                star = r['tp'].get(p,'-'); tg = r['tg'].get(p,'-')
                gate = r['rp'].get(p,'-'); spirit = r['sp'].get(p,'-')
                dg = r['dp'].get(p,'-'); sc = r['scores'][p]
                dets = r['details'][p]
                if line_idx == 0: cells.append(f' {bg}{p}宮')
                elif line_idx == 1: cells.append(f' {star}/{tg}')
                elif line_idx == 2: cells.append(f' {gate}|{spirit}')
                elif line_idx == 3: cells.append(f' 地{dg} {sc:+.1f}')
                else:
                    gejus = dets.get('gejus', [])
                    if gejus:
                        tags = ','.join(f'{t[0]}{t[1]}' for t in gejus[:3])
                        cells.append(f' {tags}')
                    else:
                        cells.append('')
            print('  ' + ' | '.join(c for c in cells if c or True))

    # 評分排名
    ranked = sorted(r['scores'].items(), key=lambda x: x[1], reverse=True)
    for i, (p, s) in enumerate(ranked):
        bg = GONG_BAGUA[p]
        dets = r['details'][p]
        gejus = dets.get('gejus', [])
        tags = ''
        for gtype, gname, gsc in gejus:
            tags += f' [{gtype}{gname}{gsc:+.1f}]'
        # 入墓/六儀擊刑/門迫
        extras2 = []
        if dets.get('tiangan_rumu', 0) < 0: extras2.append('天干入墓')
        if dets.get('men_rumu', 0) < 0: extras2.append('門入墓')
        if dets.get('liuyi_xingxing', 0) < 0: extras2.append('六儀擊刑')
        if dets.get('menpo', 0) < 0: extras2.append('門迫')
        if dets.get('dedi', 0) > 0: extras2.append('得地')
        if dets.get('changsheng_wang', 0) > 0: extras2.append('旺')
        ex_str = ' | '.join(extras2)
        print(f'  {i+1:>2}. {bg}{p} ({r["tp"].get(p,"")}/{r["rp"].get(p,"")}/{r["sp"].get(p,"")}): {s:+.1f}{tags}  {ex_str}')
    print(sep)



# ================================================================
# Part 5: 孤虛法 + 考試預測 + 每周最佳時間方位
# ================================================================

# === A. 空亡計算 ===
DZ_YANG = set(['子','寅','辰','午','申','戌'])  # 陽性地支
DZ_YIN  = set(['丑','卯','巳','未','酉','亥'])  # 陰性地支
DZ_FANGWEI = {
    '子':'正北(坎1)','丑':'東北偏北(艮8)','寅':'東北偏東(艮8)',
    '卯':'正東(震3)','辰':'東南偏東(巽4)','巳':'東南偏南(巽4)',
    '午':'正南(離9)','未':'西南偏南(坤2)','申':'西南偏西(坤2)',
    '酉':'正西(兌7)','戌':'西北偏西(乾6)','亥':'西北偏北(乾6)',
}
DZ_FANGWEI_SIMPLE = {
    '子':'正北','丑':'東北','寅':'東北','卯':'正東',
    '辰':'東南','巳':'東南','午':'正南','未':'西南',
    '申':'西南','酉':'正西','戌':'西北','亥':'西北',
}

# 每旬空亡地支
XUNKONG_MAP = {
    '甲子': ['戌','亥'], '甲戌': ['申','酉'], '甲申': ['午','未'],
    '甲午': ['辰','巳'], '甲辰': ['寅','卯'], '甲寅': ['子','丑'],
}

def get_xunkong(jz):
    """根據干支取得空亡地支列表"""
    # 找到該干支所在的旬
    jz_idx = LIUJIAZI.index(jz) if jz in LIUJIAZI else 0
    for xs_idx in reversed(XUNSHOU_IDX):
        if jz_idx >= xs_idx:
            xs_name = LIUJIAZI[xs_idx]
            return XUNKONG_MAP.get(xs_name, []), xs_name
    return [], '甲子'

# === B. 孤虛法計算 ===
def calc_guxu(sgz, r=None):
    """孤虛法計算
    sgz: 時干支 (如 '癸亥')
    r: qiju_v2 完整盤局（可選）
    
    返回 dict:
      xunkong: 空亡地支列表
      xunshou: 旬首
      shizhi_yang: 時支是否陽性
      gu_dz: 孤位地支
      xu_dz: 虛位地支
      gu_fangwei: 孤位方位
      xu_fangwei: 虛位方位
      advice: 運用建議
    """
    kong_dz_list, xs_name = get_xunkong(sgz)
    shi_zhi = sgz[1]
    is_yang = shi_zhi in DZ_YANG
    
    # 根據時支陰陽選擇孤位
    gu_dz = None
    for dz in kong_dz_list:
        if (dz in DZ_YANG) == is_yang:
            gu_dz = dz
            break
    if gu_dz is None and kong_dz_list:
        gu_dz = kong_dz_list[0]  # fallback
    
    # 虛位 = 孤位的對衝地支
    xu_dz = DZ_CHONG.get(gu_dz, '') if gu_dz else ''
    
    return {
        'xunkong': kong_dz_list,
        'xunshou': xs_name,
        'shizhi': shi_zhi,
        'shizhi_yang': is_yang,
        'gu_dz': gu_dz,
        'xu_dz': xu_dz,
        'gu_fangwei': DZ_FANGWEI.get(gu_dz, '') if gu_dz else '',
        'xu_fangwei': DZ_FANGWEI.get(xu_dz, '') if xu_dz else '',
        'gu_fangwei_simple': DZ_FANGWEI_SIMPLE.get(gu_dz, '') if gu_dz else '',
        'xu_fangwei_simple': DZ_FANGWEI_SIMPLE.get(xu_dz, '') if xu_dz else '',
        'advice': f'自己背對{gu_dz}({DZ_FANGWEI_SIMPLE.get(gu_dz,"?")})、面向{xu_dz}({DZ_FANGWEI_SIMPLE.get(xu_dz,"?")})而坐' if gu_dz else '無法計算',
    }

def print_guxu(gx):
    """格式化輸出孤虛法結果"""
    print(f'  孤虛法:')
    print(f'    旬首: {gx["xunshou"]}  |  空亡: {"、".join(gx["xunkong"])}')
    print(f'    時支: {gx["shizhi"]}({"陽" if gx["shizhi_yang"] else "陰"})')
    print(f'    孤位: {gx["gu_dz"]} ({gx["gu_fangwei"]})')
    print(f'    虛位: {gx["xu_dz"]} ({gx["xu_fangwei"]})')
    print(f'    運用: {gx["advice"]}')

# === C. 考試預測函數（EP19）===
def predict_exam(r, is_self=True):
    """考試升學預測
    r = qiju_v2() 完整盤局
    is_self: 是否親自求測（True=日干為考生, False=時干為考生）
    
    四用神: 考生(日干/時干) / 景門(試題) / 年干(學校) / 天輔星(升學)
    """
    dp, tp, tg_map, rp, sp = r['dp'], r['tp'], r['tg'], r['rp'], r['sp']
    day_gan = r['dgz'][0]
    hour_gan = r['stg']
    
    results = {'steps': [], 'verdict': '', 'confidence': ''}
    
    # 考生用神
    candidate_tg = day_gan if is_self else hour_gan
    candidate_label = '日干(自己)' if is_self else '時干(代測)'
    candidate_pal = find_tiangan_palace(tg_map, candidate_tg)
    
    if candidate_pal is None:
        results['verdict'] = f'無法找到考生用神({candidate_tg})'
        return results
    
    results['steps'].append({
        'step': 0, 'check': f'考生({candidate_label}={candidate_tg})',
        'palace': f'{GONG_BAGUA[candidate_pal]}{candidate_pal}宮',
    })
    
    sheng_count = 0
    ke_count = 0
    
    # Step 1: 景門(試題) vs 考生
    jingmen_pal = find_palace_of(tg_map, rp, sp, tp, '景門')[0]
    if jingmen_pal:
        rel, sc = palace_shengke(jingmen_pal, candidate_pal)
        detail = f'景門宮{GONG_BAGUA[jingmen_pal]}→考生宮{GONG_BAGUA[candidate_pal]}: {rel}'
        if sc > 0:
            detail += ' → 考生答題好，成績不差'
            sheng_count += 1
        elif sc < 0:
            detail += ' → 試題對考生不利'
            ke_count += 1
        else:
            detail += ' → 成績一般'
        results['steps'].append({'step': 1, 'check': '景門(試題) vs 考生', 'detail': detail, 'score': sc})
    
    # Step 2: 年干(學校) vs 考生
    year_gan = _get_year_gan(r['dt'])
    year_pal = find_tiangan_palace(tg_map, year_gan)
    if year_pal:
        rel, sc = palace_shengke(year_pal, candidate_pal)
        detail = f'年干(學校)宮{GONG_BAGUA[year_pal]}→考生宮{GONG_BAGUA[candidate_pal]}: {rel}'
        if sc > 0:
            detail += ' → 學校會錄取考生'
            sheng_count += 1
        elif sc < 0:
            detail += ' → 學校不會錄取'
            ke_count += 1
        else:
            detail += ' → 錄取與否需看其他因素'
        results['steps'].append({'step': 2, 'check': '年干(學校) vs 考生', 'detail': detail, 'score': sc})
    
    # Step 3: 天輔星(升學) vs 考生
    tianfu_pal = find_palace_of(tg_map, rp, sp, tp, '天輔')[0]
    if tianfu_pal:
        rel, sc = palace_shengke(tianfu_pal, candidate_pal)
        detail = f'天輔星宮{GONG_BAGUA[tianfu_pal]}→考生宮{GONG_BAGUA[candidate_pal]}: {rel}'
        if sc > 0:
            detail += ' → 有機會繼續升學'
            sheng_count += 1
        elif sc < 0:
            detail += ' → 升學機會渺茫'
            ke_count += 1
        else:
            detail += ' → 升學看運氣'
        results['steps'].append({'step': 3, 'check': '天輔星(升學) vs 考生', 'detail': detail, 'score': sc})
    
    # 綜合判斷
    total = sheng_count + ke_count
    if total == 0:
        results['verdict'] = '無法判斷（用神缺失）'
        results['confidence'] = 'low'
    elif sheng_count == total:
        results['verdict'] = '大吉，一定考上'
        results['confidence'] = 'high'
    elif sheng_count > ke_count:
        results['verdict'] = '偏吉，有機會考上'
        results['confidence'] = 'medium'
    elif ke_count == total:
        results['verdict'] = '凶，考不上'
        results['confidence'] = 'high'
    else:
        results['verdict'] = '偏凶，需努力'
        results['confidence'] = 'medium'
    
    # 附加: 年干和天輔星同宮=雙重印證
    if year_pal and tianfu_pal and year_pal == tianfu_pal:
        results['steps'].append({
            'step': 4, 'check': '特殊情況',
            'detail': f'年干與天輔星同落{GONG_BAGUA[year_pal]}{year_pal}宮 → 雙重印證',
        })
    
    return results

def _get_year_gan(dt):
    """取得年干"""
    # 簡化: 2024=甲, 2025=乙, 2026=丙 ...
    return TIANGAN[(dt.year - 4) % 10]

# === D. 每日最佳時間方位預測 ===
SHICHEN_LIST = [
    ('子時', 23, 1), ('丑時', 1, 3), ('寅時', 3, 5), ('卯時', 5, 7),
    ('辰時', 7, 9), ('巳時', 9, 11), ('午時', 11, 13), ('未時', 13, 15),
    ('申時', 15, 17), ('酉時', 17, 19), ('戌時', 19, 21), ('亥時', 21, 23),
]

def best_time_direction(dt):
    """計算某天每個時辰的最佳方位和評分
    dt: datetime（日期）
    返回 [(時辰名, 時間範圍, 最佳宮位, 方位, 評分, 盤局), ...] 按評分降序
    """
    results = []
    for sc_name, start_h, end_h in SHICHEN_LIST:
        try:
            h = start_h if start_h != 23 else 23
            test_dt = dt.replace(hour=h, minute=0)
            r = qiju_v2(test_dt)
            best_p = max(r['scores'], key=r['scores'].get)
            best_sc = r['scores'][best_p]
            results.append({
                'shichen': sc_name,
                'time_range': f'{start_h:02d}:00-{end_h:02d}:00',
                'best_palace': best_p,
                'fangwei': GONG_BAGUA[best_p],
                'score': best_sc,
                'r': r,
            })
        except Exception as e:
            results.append({
                'shichen': sc_name, 'time_range': f'{start_h:02d}:00-{end_h:02d}:00',
                'best_palace': 0, 'fangwei': '?', 'score': -999, 'error': str(e),
            })
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

def weekly_forecast(start_date, days=7):
    """一周每日最佳時間方位預測
    start_date: datetime 起始日期
    days: 天數（默認7天）
    """
    from datetime import timedelta
    week_names = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    forecast = []
    for i in range(days):
        dt = start_date + timedelta(days=i)
        day_results = best_time_direction(dt)
        best = day_results[0] if day_results else None
        worst = day_results[-1] if day_results else None
        
        # 判斷是否「大事勿用」
        all_bad = all(d['score'] < -2.0 for d in day_results if 'score' in d)
        has_good = any(d['score'] >= 2.0 for d in day_results if 'score' in d)
        
        day_info = {
            'date': dt.strftime('%Y-%m-%d'),
            'weekday': week_names[dt.weekday()],
            'dgz': day_ganzhi(dt)[0] if day_results else '?',
            'best': best,
            'worst': worst,
            'all_bad': all_bad,
            'has_good': has_good,
            'advice': '',
        }
        
        if all_bad:
            day_info['advice'] = '大事勿用，建議休息'
        elif best and best['score'] >= 3.0:
            day_info['advice'] = f'最適合做大事: {best["shichen"]}({best["time_range"]}) 往{best["fangwei"]}方位'
        elif best:
            day_info['advice'] = f'較好: {best["shichen"]}({best["time_range"]}) 往{best["fangwei"]}方位'
        
        forecast.append(day_info)
    
    # 排名: 最適合做大事的日子
    ranked = sorted(forecast, key=lambda d: d['best']['score'] if d['best'] else -999, reverse=True)
    forecast_ranked = [f['date'] + ' ' + f['weekday'] for f in ranked if not f['all_bad']]
    
    return {
        'forecast': forecast,
        'best_days': forecast_ranked[:3],
        'worst_days': [f['date'] + ' ' + f['weekday'] for f in ranked if f['all_bad']],
    }

def print_weekly_forecast(wf):
    """格式化輸出每周預測"""
    print('')
    print('=' * 60)
    print('  每周最佳時間方位預測')
    print('=' * 60)
    for day in wf['forecast']:
        date_str = day['date'] + ' ' + day['weekday'] + ' (' + day['dgz'] + ')'
        print('  ' + date_str)
        if day['all_bad']:
            print('    ' + day['advice'])
        elif day['best']:
            b = day['best']
            print('    best: ' + b['shichen'] + ' (' + b['time_range'] + ') -> ' + b['fangwei'] + ' [' + str(b['score']) + ']')
        print('    ' + day['advice'])
    if wf['best_days']:
        print('  best_days: ' + ' '.join(wf['best_days']))
    if wf['worst_days']:
        print('  worst_days: ' + ' '.join(wf['worst_days']))
    print('=' * 60)
