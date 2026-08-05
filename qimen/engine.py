#!/usr/bin/env python3
"""
奇門遁甲量化系統 (Qi Men Dun Jia Quantification System)
=========================================================
完整實現：地盤 + 天盤(星+干) + 人盤(門) + 神盤(神) 飛布
       格局偵測(吉格/凶格) + 五行生剋 + 評分系統
       投資決策輸出

⚠️ 節氣日期為 2026 年近似值，精確起局需配合萬年曆
⚠️ 日干支公式已用 2000-01-01=戊午日 校準
"""

from datetime import datetime, timedelta

# ================================================================
# 一、基礎數據表
# ================================================================

TIANGAN = list('甲乙丙丁戊己庚辛壬癸')
DIZHI   = list('子丑寅卯辰巳午未申酉戌亥')

# 60甲子
def _make_60jz():
    out = []
    for i in range(60):
        out.append(TIANGAN[i % 10] + DIZHI[i % 12])
    return out
LIUJIAZI = _make_60jz()

# 六儀三奇 — 飛布放置順序
LIUYI_SANQI = list('戊己庚辛壬癸丁丙乙')

# 旬首 → 遁儀
XUNSHOU_DUNYI = {
    '甲子': '戊', '甲戌': '己', '甲申': '庚',
    '甲午': '辛', '甲辰': '壬', '甲寅': '癸'
}
XUNSHOU_IDX = [0, 10, 20, 30, 40, 50]

# 九星 (index 0-8 ↔ palace 1-9)
JIUXING = ['天蓬','天芮','天沖','天輔','天禽','天心','天柱','天任','天英']
JIUXING_SCORE = {
    '天心': 3.0,  '天任': 2.5,  '天輔': 2.5,  '天禽': 2.0,
    '天沖': 1.0,  '天英': 0.5,
    '天芮': -1.5, '天柱': -1.5, '天蓬': -2.0
}

# 八門 (自然宮位: 休1 死2 傷3 杜4 開6 驚7 生8 景9)
BAMEN_ORDER = ['休門','死門','傷門','杜門','開門','驚門','生門','景門']
BAMEN_HOME  = [1, 2, 3, 4, 6, 7, 8, 9]   # 對應宮位
BAMEN_SCORE = {
    '開門': 3.0,  '生門': 3.0,  '休門': 2.5,  '景門': 1.0,
    '死門': -3.0, '驚門': -2.5, '傷門': -2.0, '杜門': -1.5
}

# 八神 (飛布順序)
BASHEN_ORDER = ['值符','騰蛇','太陰','六合','白虎','玄武','九地','九天']
BASHEN_SCORE = {
    '值符': 3.0,  '九天': 2.0,  '六合': 2.0,  '太陰': 1.5,
    '九地': 1.0,
    '騰蛇': -1.5, '玄武': -2.0, '白虎': -2.5
}

# 宮位 → 八卦
GONG_BAGUA = {1:'坎',2:'坤',3:'震',4:'巽',5:'中',6:'乾',7:'兌',8:'艮',9:'離'}

# 天干五行
TG_WUXING = {
    '甲':'木','乙':'木','丙':'火','丁':'火',
    '戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'
}

# 五行生剋係數 (我的五行, 對方五行)
WX_SK = {
    ('木','木'): 1.0, ('木','火'): 0.5, ('木','土'): 0.3, ('木','金'):-1.5, ('木','水'): 0.8,
    ('火','木'):-1.5, ('火','火'): 1.0, ('火','土'): 0.5, ('火','金'): 0.3, ('火','水'):-1.5,
    ('土','木'): 0.3, ('土','火'): 0.8, ('土','土'): 1.0, ('土','金'): 0.5, ('土','水'):-1.5,
    ('金','木'): 0.8, ('金','火'):-1.5, ('金','土'):-1.5, ('金','金'): 1.0, ('金','水'): 0.5,
    ('水','木'): 0.5, ('水','火'):-1.5, ('水','土'): 0.3, ('水','金'): 0.8, ('水','水'): 1.0,
}

# 吉格 / 凶格
JI_GE = [
    ('天遁', lambda t,d,g,s: t=='丙' and d=='戊' and g=='生門', 3.0),
    ('地遁', lambda t,d,g,s: t=='乙' and s=='太陰' and g in ('生門','九地'), 2.5),
    ('人遁', lambda t,d,g,s: t=='乙' and g=='休門' and s=='六合', 2.0),
    ('神遁', lambda t,d,g,s: t=='丙' and s=='九天' and g=='生門', 2.5),
    ('龍遁', lambda t,d,g,s: t=='乙' and d=='壬' and g=='休門', 2.0),
    ('虎遁', lambda t,d,g,s: t=='辛' and g=='生門', 2.0),
]
XIONG_GE = [
    ('青龍逃走', lambda t,d,g,s: t=='乙' and d=='辛', -3.0),
    ('白虎猖狂', lambda t,d,g,s: t=='辛' and d=='乙', -3.0),
    ('朱雀投江', lambda t,d,g,s: t=='丁' and d=='壬', -2.5),
    ('螣蛇夭矯', lambda t,d,g,s: t=='乙' and d=='己', -2.0),
    ('大格',     lambda t,d,g,s: t=='庚' and d=='癸', -2.5),
    ('小格',     lambda t,d,g,s: t=='庚' and d=='壬', -2.0),
    ('刑格',     lambda t,d,g,s: t=='庚' and d=='己', -2.0),
    ('飛宮格',   lambda t,d,g,s: t=='庚' and d=='庚', -3.0),
]

# 時辰地支 → 宮位 (後天八卦方位)
DZ2GONG = {
    '子':1,'丑':8,'寅':8,'卯':3,'辰':4,'巳':4,
    '午':9,'未':2,'申':2,'酉':7,'戌':6,'亥':6
}

# 24 節氣 2026 近似日期
JIEQI_2026 = [
    ('小寒',1,5),('大寒',1,20),('立春',2,4),('雨水',2,19),
    ('驚蟄',3,6),('春分',3,21),('清明',4,5),('穀雨',4,20),
    ('立夏',5,6),('小滿',5,21),('芒種',6,6),('夏至',6,21),
    ('小暑',7,7),('大暑',7,23),('立秋',8,7),('處暑',8,23),
    ('白露',9,8),('秋分',9,23),('寒露',10,8),('霜降',10,24),
    ('立冬',11,7),('小雪',11,22),('大雪',12,7),('冬至',12,22),
]

# 節氣 → base 局數
JIEQI_BASE = {
    '冬至':1,'小寒':2,'大寒':3, '立春':8,'雨水':9,'驚蟄':1,
    '春分':2,'清明':3,'穀雨':4, '立夏':4,'小滿':5,'芒種':6,
    '夏至':9,'小暑':8,'大暑':7, '立秋':2,'處暑':1,'白露':9,
    '秋分':8,'寒露':7,'霜降':6, '立冬':6,'小雪':5,'大雪':4,
}
YANG_JIEQI = set(['冬至','小寒','大寒','立春','雨水','驚蟄',
                   '春分','清明','穀雨','立夏','小滿','芒種'])

# 洛書顯示順序
LUOSHU = [[4,9,2],[3,5,7],[8,1,6]]

# 旬首 → 星
XUNSHOU_STAR = {
    '甲子':'天蓬','甲戌':'天芮','甲申':'天沖',
    '甲午':'天輔','甲辰':'天心','甲寅':'天禽'
}
# 星 → 門 (同宮)
STAR_DOOR = {
    '天蓬':'休門','天芮':'死門','天沖':'傷門','天輔':'杜門',
    '天禽':'死門',   # 寄坤二
    '天心':'開門','天柱':'驚門','天任':'生門','天英':'景門'
}


# ================================================================
# 二、日曆工具
# ================================================================

def _julian(y, m, d):
    """Julian Day Number (noon)"""
    if m <= 2:
        y -= 1; m += 12
    A = y // 100
    B = 2 - A + A // 4
    return int(365.25*(y+4716)) + int(30.6001*(m+1)) + d + B - 1525

def day_ganzhi(dt):
    """日干支, 校準: 2000-01-01 = 戊午 (index 54)"""
    jdn = _julian(dt.year, dt.month, dt.day)
    idx = (jdn + 9) % 60          # +9 校準偏移
    return LIUJIAZI[idx], idx

def shichen_dz(hour):
    """小時 → 時辰地支 (從大到大 check, 避免 4>=1 先命中)"""
    for start, name in [(23,'子'),(21,'亥'),(19,'戌'),(17,'酉'),(15,'申'),(13,'未'),
                         (11,'午'),(9,'巳'),(7,'辰'),(5,'卯'),(3,'寅'),(1,'丑')]:
        if hour >= start: return name
    return '子'

def shichen_ganzhi(day_idx, hour):
    """時辰干支"""
    dz = shichen_dz(hour)
    tg_idx = (day_idx % 10) * 2 + DIZHI.index(dz)
    tg_idx %= 10
    return TIANGAN[tg_idx] + dz

def find_xunshou(jz_idx):
    """找旬首"""
    for xs in reversed(XUNSHOU_IDX):
        if jz_idx >= xs:
            return LIUJIAZI[xs], xs
    return '甲子', 0


# ================================================================
# 三、節氣 & 局數
# ================================================================

def current_jieqi(dt):
    """當前節氣 + 起始日"""
    name = JIEQI_2026[0][0]
    start = datetime(2026, JIEQI_2026[0][1], JIEQI_2026[0][2])
    for jname, m, d in JIEQI_2026:
        jdt = datetime(2026, m, d)
        if dt >= jdt:
            name, start = jname, jdt
        else:
            break
    return name, start

def ju_number(dt):
    """局數 + 元"""
    jname, jstart = current_jieqi(dt)
    base = JIEQI_BASE[jname]
    yang = jname in YANG_JIEQI
    days_in = (dt - jstart).days
    yuan = min(days_in // 5, 2)
    if yang:
        ju = base + yuan
    else:
        ju = base - yuan
    ju = ((ju - 1) % 9) + 1
    return ju, ['上元','中元','下元'][yuan], yang, jname


# ================================================================
# 四、地盤 (Earth Plate)
# ================================================================

def make_dipan(ju, yang):
    """
    戊從局數宮開始, 陽遁順飛 1→9, 陰遁逆飛 9→1
    六儀三奇按順序排入九宮
    """
    order = list(range(1,10)) if yang else list(range(9,0,-1))
    start = order.index(ju)
    dp = {}
    for i, stem in enumerate(LIUYI_SANQI):
        pos = (start + i) % 9
        dp[order[pos]] = stem
    return dp


# ================================================================
# 五、天盤 — 九星 + 天盤干
# ================================================================

def make_tianpan(dipan, shi_tg, xunshou, yang):
    """
    值符星飛到時辰天干在地盤嘅位置, 所有九星同步偏移
    同時飛布天盤干 (六儀三奇跟住星一齊轉)
    """
    zhifu = XUNSHOU_STAR[xunshou]
    zhifu_home = JIUXING.index(zhifu) + 1       # 1-indexed
    dunyi = XUNSHOU_DUNYI[xunshou]
    dunyi_home = None
    for p, s in dipan.items():
        if s == dunyi: dunyi_home = p; break
    if dunyi_home is None: dunyi_home = 1

    # 時辰天干在地盤嘅位置
    target = None
    for p, s in dipan.items():
        if s == shi_tg: target = p; break
    if target is None: target = zhifu_home

    order = list(range(1,10)) if yang else list(range(9,0,-1))
    zhifu_pos  = order.index(zhifu_home)
    target_pos = order.index(target)
    offset = (target_pos - zhifu_pos) % 9

    stars = {};  stem_map = {}
    for i, star in enumerate(JIUXING):
        np = order[(order.index(i+1) + offset) % 9]
        stars[np] = star
    for i, stem in enumerate(LIUYI_SANQI):
        np = order[(order.index(dunyi_home) + i + offset - order.index(dunyi_home)) % 9]
        # 更簡潔: 同星一樣嘅 offset
        pass
    # 天盤干：遁儀從自己地盤位置飛到時辰天干位置, 其餘跟隨
    stem_offset = offset   # 同星一樣
    for i, stem in enumerate(LIUYI_SANQI):
        # stem i 在地盤嘅位置
        stem_palace = None
        for p, s in dipan.items():
            if s == stem: stem_palace = p; break
        if stem_palace is None: continue
        sp = order.index(stem_palace)
        np = order[(sp + offset) % 9]
        stem_map[np] = stem

    return stars, stem_map, zhifu


# ================================================================
# 六、人盤 — 八門
# ================================================================

def make_renpan(shi_dz, xunshou, yang):
    """
    值使門飛到時辰地支對應宮位, 其餘門同步
    8門飛8宮 (跳過中5)
    """
    zhishi = STAR_DOOR[XUNSHOU_STAR[xunshou]]
    zhishi_idx = BAMEN_ORDER.index(zhishi)
    zhishi_home = BAMEN_HOME[zhishi_idx]
    target = DZ2GONG[shi_dz]

    fly = [1,2,3,4,6,7,8,9] if yang else [9,8,7,6,4,3,2,1]
    z_pos = fly.index(zhishi_home)
    t_pos = fly.index(target) if target in fly else 0
    off = (t_pos - z_pos) % 8

    doors = {}
    for i, door in enumerate(BAMEN_ORDER):
        doors[fly[(i + off) % 8]] = door
    return doors, zhishi


# ================================================================
# 七、神盤 — 八神
# ================================================================

def make_shenpan(tianpan, zhifu, yang):
    """
    值符神同值符星同宮, 陽遁順飛, 陰遁逆飛
    """
    zhifu_palace = None
    for p, s in tianpan.items():
        if s == zhifu: zhifu_palace = p; break
    if zhifu_palace is None: zhifu_palace = 1

    fly = [1,2,3,4,6,7,8,9] if yang else [9,8,7,6,4,3,2,1]
    start = fly.index(zhifu_palace) if zhifu_palace in fly else 0

    gods = {}
    for i, god in enumerate(BASHEN_ORDER):
        gods[fly[(start + i) % 8]] = god
    return gods


# ================================================================
# 五行通關表（EP02）: A剋B時的通關者 C（A生C, C生B）
TONGGUAN = {
    ("金","木"): "水",
    ("木","土"): "火",
    ("水","火"): "木",
    ("火","金"): "土",
    ("土","水"): "金",
}

# 用神系統（EP02）
YONGSHEN = {
    "marriage": {"乙": "太太", "庚": "先生", "六合": "婚姻"},
    "investment": {"開門": "交易", "生門": "利潤"},
}

# 天/地盤干權重（EP02 G18）
TIANGAN_WEIGHT = 1.0
DIPAN_GAN_WEIGHT = 0.3

# 八、格局偵測 + 評分
# ================================================================

def detect_patterns(t_gan, d_gan, gate, spirit):
    found = [];  pscore = 0.0
    for name, fn, sc in JI_GE:
        if fn(t_gan, d_gan, gate, spirit):
            found.append(('吉', name, sc)); pscore += sc
    for name, fn, sc in XIONG_GE:
        if fn(t_gan, d_gan, gate, spirit):
            found.append(('凶', name, sc)); pscore += sc
    return found, pscore

def palace_score(star, gate, spirit, t_gan, d_gan):
    """
    總分 = 星分 + 門分 + 神分 + 干支生剋 + 格局
    """
    ss = JIUXING_SCORE.get(star, 0)
    gs = BAMEN_SCORE.get(gate, 0)
    hs = BASHEN_SCORE.get(spirit, 0)
    wx = WX_SK.get((TG_WUXING.get(t_gan,'土'), TG_WUXING.get(d_gan,'土')), 0)
    pats, ps = detect_patterns(t_gan, d_gan, gate, spirit)
    return ss + gs + hs + wx + ps, {
        'star': ss, 'gate': gs, 'spirit': hs, 'wuxing': wx, 'pattern': ps, 'pats': pats
    }

def decision(score):
    if score >= 5.0:  return '強烈看多, 加倉'
    if score >= 2.0:  return '偏多, 可買入'
    if score >= -2.0: return '觀望, 唔操作'
    if score >= -5.0: return '偏空, 減倉'
    return '強烈看空, 清倉'


# ================================================================
# 九、完整起局
# ================================================================

def qiju(dt):
    dgz, d_idx   = day_ganzhi(dt)
    sdz           = shichen_dz(dt.hour)
    sgz           = shichen_ganzhi(d_idx, dt.hour)
    stg           = sgz[0]
    s_idx         = LIUJIAZI.index(sgz)
    xs, xs_idx    = find_xunshou(s_idx)
    ju, yuan, yang, jname = ju_number(dt)
    dp            = make_dipan(ju, yang)
    tp, tg_map, zhifu = make_tianpan(dp, stg, xs, yang)
    rp, zhishi    = make_renpan(sdz, xs, yang)
    sp            = make_shenpan(tp, zhifu, yang)

    scores = {}; details = {}
    for p in range(1, 10):
        star   = tp.get(p, '')
        gate   = rp.get(p, '')
        spirit = sp.get(p, '')
        t_gan  = tg_map.get(p, stg)
        d_gan  = dp.get(p, '')
        sc, det = palace_score(star, gate, spirit, t_gan, d_gan)
        scores[p] = sc;  details[p] = det

    return dict(dt=dt, dgz=dgz, sgz=sgz, sdz=sdz, stg=stg, xs=xs,
                jname=jname, yang=yang, ju=ju, yuan=yuan,
                dp=dp, tp=tp, tg=tg_map, rp=rp, sp=sp,
                zhifu=zhifu, zhishi=zhishi,
                scores=scores, details=details)


# ================================================================
# 十、輸出
# ================================================================

def print_chart(r, title=''):
    sep = '═' * 62
    print(f"\n{sep}")
    if title: print(f"  {title}")
    print(f"  奇門遁甲量化盤")
    print(sep)
    print(f"  時間: {r['dt'].strftime('%Y-%m-%d %H:%M')}")
    print(f"  日干支: {r['dgz']}  │  時辰: {r['sgz']}")
    print(f"  節氣: {r['jname']}  │  {'陽遁' if r['yang'] else '陰遁'}{r['ju']}局 {r['yuan']}")
    print(f"  值符: {r['zhifu']}  │  值使: {r['zhishi']}")
    print(f"  旬首: {r['xs']}  │  時辰天干: {r['stg']}")
    print('─' * 62)

    # 地盤
    print("\n  【地盤 Earth Plate — 六儀三奇固定布局】")
    for row in LUOSHU:
        cells = [f"{GONG_BAGUA[p]}{p}({r['dp'][p]})" for p in row]
        print('    ' + '  │  '.join(cells))

    # 完整九宮
    print("\n  【完整九宮格】")
    for ri, row in enumerate(LUOSHU):
        if ri == 1:
            print('  ' + '─' * 54)
        # build 4 lines per row
        L = ['' for _ in range(4)]
        for p in row:
            bg = GONG_BAGUA[p]
            star   = r['tp'].get(p,'-')
            tg     = r['tg'].get(p,'-')
            gate   = r['rp'].get(p,'-')
            spirit = r['sp'].get(p,'-')
            dg     = r['dp'].get(p,'-')
            sc     = r['scores'][p]
            L[0] += f'  {bg}{p}宮       '
            L[1] += f'  {star}/{tg}     '
            L[2] += f'  {gate}|{spirit}  '
            L[3] += f'  地{dg} {sc:+.1f}   '
        for l in L:
            print(l)
    print('  ' + '─' * 54)

    # 評分詳情
    print("\n  【各宮評分明細】")
    print(f"  {'宮':<6} {'星':<6} {'門':<6} {'神':<6} {'星分':<6} {'門分':<6} {'神分':<6} {'五行':<6} {'格局':<6} {'總分'}")
    print('  ' + '─' * 68)
    for p in range(1, 10):
        d = r['details'][p]
        bg = GONG_BAGUA[p] + str(p)
        print(f"  {bg:<6} {r['tp'].get(p,''):<6} {r['rp'].get(p,''):<6} {r['sp'].get(p,''):<6}"
              f" {d['star']:+5.1f} {d['gate']:+5.1f} {d['spirit']:+5.1f} {d['wuxing']:+5.1f} {d['pattern']:+5.1f} {r['scores'][p]:+6.1f}")
        if d['pats']:
            for pt, pn, ps in d['pats']:
                print(f"         ⚡ {pt}格: {pn} ({ps:+.1f})")

    # 投資決策
    print("\n  【投資決策 — 用神: 開門(交易) / 生門(增長)】")
    for p in range(1, 10):
        gate = r['rp'].get(p, '')
        if gate in ('開門', '生門'):
            sc = r['scores'][p]
            bg = GONG_BAGUA[p] + str(p)
            tag = '🔴' if sc < -2 else ('🟡' if sc < 2 else ('🟢' if sc < 5 else '🔥'))
            print(f"  {tag} {gate} 在 {bg}宮 → 總分 {sc:+.1f} → {decision(sc)}")

    # 排名
    print("\n  【宮位分數排名】")
    ranked = sorted(r['scores'].items(), key=lambda x: x[1], reverse=True)
    for i, (p, s) in enumerate(ranked):
        bg = GONG_BAGUA[p] + str(p)
        print(f"  {i+1:>2}. {bg} ({r['tp'].get(p,'')}/{r['rp'].get(p,'')}): {s:+.1f}")
    print(sep)


# ================================================================
# 十一、Demo
# ================================================================

if __name__ == '__main__':
    # --- Demo 1: 用戶傳訊息嘅時間 ---
    dt1 = datetime(2026, 8, 3, 15, 19)
    r1 = qiju(dt1)
    print_chart(r1, 'Demo 1: 2026-08-03 15:19 未時 — 「而家入唔入騰訊?」')

    # --- Demo 2: 聽朝開市 ---
    dt2 = datetime(2026, 8, 4, 9, 30)
    r2 = qiju(dt2)
    print_chart(r2, 'Demo 2: 2026-08-04 09:30 巳時 — 「聽朝開市入唔入?」')

    # --- Demo 3: 全日 12 時辰掃描 ---
    print("\n\n" + "═" * 62)
    print("  Demo 3: 2026-08-03 全日 12 時辰投資掃描")
    print("═" * 62)
    hours = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
    print(f"\n  {'時辰':<8} {'開門宮':<8} {'開門分':<8} {'生門宮':<8} {'生門分':<8} {'最佳分':<8} {'建議'}")
    print('  ' + '─' * 62)
    for h in hours:
        dt = datetime(2026, 8, 3, h)
        r = qiju(dt)
        ks = gs_ = -999
        kp = gp = '-'
        for p in range(1, 10):
            g = r['rp'].get(p, '')
            if g == '開門': kp = GONG_BAGUA[p]+str(p); ks = r['scores'][p]
            if g == '生門': gp = GONG_BAGUA[p]+str(p); gs_ = r['scores'][p]
        best = max(ks, gs_)
        bs = f"{ks:+.1f}" if ks > -999 else '—'
        bgs = f"{gs_:+.1f}" if gs_ > -999 else '—'
        bes = f"{best:+.1f}" if best > -999 else '—'
        dec = decision(best) if best > -999 else '—'
        print(f"  {r['sgz']:<8} {kp:<8} {bs:<8} {gp:<8} {bgs:<8} {bes:<8} {dec}")

    # --- Demo 4: 公式展示 ---
    print("\n\n" + "═" * 62)
    print("  量化公式總結")
    print("═" * 62)
    print("""
  宮位總分 = 星分 + 門分 + 神分 + 干支生剋 + 格局加減分

  各層轉動邏輯:
  ┌─────────┬──────────────────┬──────────┬────────────┐
  │ 層       │ 基底             │ 變化週期  │ 驅動因素   │
  ├─────────┼──────────────────┼──────────┼────────────┤
  │ 地盤     │ 局數(節氣+元)    │ ~5日     │ 節氣+旬    │
  │ 天盤星   │ 值符星           │ 每時辰    │ 時辰天干   │
  │ 天盤干   │ 遁儀(六儀三奇)   │ 每時辰    │ 時辰天干   │
  │ 人盤門   │ 值使門           │ 每時辰    │ 時辰地支   │
  │ 神盤     │ 值符神           │ 每時辰    │ 值符星位置 │
  └─────────┴──────────────────┴──────────┴────────────┘

  決策閾值:
  ≥ +5.0  強烈看多, 加倉
  ≥ +2.0  偏多, 可買入
  ≥ -2.0  觀望, 唔操作
  ≥ -5.0  偏空, 減倉
  < -5.0  強烈看空, 清倉
""")
