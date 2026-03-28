# -*- coding: utf-8 -*-
"""
全面交叉校验脚本 —— 独立验算 A/B/C 三个版本的 29 项 NRC 指标
并与各文档记载值逐项对比，找出任何不一致。
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ─────────────────── 食材营养数据 (per 100g raw) ───────────────────
# 顺序: 鸡腿肉, 猪瘦肉, 鸡心, 牛心, 鸡蛋, 鸡肝, 牛肝, 鲭鱼, 鸡皮, 鸭胸肉
# 鸭胸肉 = USDA FDC 171557 "Duck, domesticated, meat only, raw"
# 能量135 蛋白18.28 脂肪5.95 — 标准USDA值
nut = {
    '能量':        [119, 143, 153, 112, 143, 119, 135, 205.4, 349, 135],
    '蛋白质':      [19.6, 21.1, 15.6, 17.7, 12.6, 16.9, 20.4, 18.6, 13.3, 18.28],
    '脂肪':        [4.3, 6.9, 9.3, 3.9, 9.9, 4.8, 3.6, 13.9, 32.4, 5.95],
    '磷':          [178, 197, 177, 212, 198, 297, 387, 217, 68, 203],
    '钙':          [9, 5, 12, 7, 56, 8, 5, 12, 11, 11],
    '铁':          [0.8, 0.8, 5.9, 4.3, 1.8, 9.0, 4.9, 1.63, 0.7, 2.4],
    '锌':          [1.8, 1.9, 6.6, 2.4, 1.3, 2.7, 4.0, 0.63, 0.6, 1.9],
    '铜':          [0.06, 0.06, 0.33, 0.39, 0.07, 0.49, 9.76, 0.07, 0.02, 0.24],
    '锰':          [0.02, 0.01, 0.05, 0.03, 0.03, 0.26, 0.31, 0.02, 0.01, 0.02],
    '钾':          [242.0, 389.0, 176.066, 286.984, 138.0, 230.0, 313.0, 314.0, 119.0, 271.0],
    '钠':          [95.0, 52.0, 73.934, 97.989, 142.0, 71.0, 69.0, 90.0, 51.0, 74.0],
    '碘':          [1, 1, 5, 5, 27, 3, 3, 44, 1, 1],
    '硒':          [23.0, 32.5, 16.0, 21.8, 30.7, 54.6, 39.7, 44.1, 14.1, 14.0],
    'VA':          [50, 7, 31, 0, 520, 11078, 16898, 167, 150, 24],
    'VD':          [5, 12, 0, 0, 82, 12, 49, 644, 0, 0],
    'VE':          [0.2, 0.5, 0.7, 0.2, 1.1, 0.7, 0.5, 1.52, 0.3, 0.7],
    'VB1':         [0.07, 0.81, 0.13, 0.24, 0.04, 0.31, 0.19, 0.18, 0.01, 0.36],
    'VB2':         [0.16, 0.23, 0.73, 0.91, 0.46, 1.78, 2.76, 0.31, 0.07, 0.47],
    'VB3':         [5.3, 5.0, 4.8, 7.4, 0.1, 9.7, 13.2, 9.08, 2.5, 5.3],
    'VB6':         [0.33, 0.42, 0.29, 0.28, 0.14, 0.85, 1.08, 0.40, 0.05, 0.34],
    'VB12':        [0.4, 0.6, 7.3, 8.6, 0.9, 16.6, 59.3, 8.7, 0.3, 0.4],
    '牛磺酸':      [40, 50, 145, 160, 20, 30, 40, 70, 10, 0],   # 鸭胸保守=0
    '花生四烯酸':  [50, 70, 84, 25, 155, 260, 200, 60, 250, 0],  # 鸭胸保守=0
    'EPA+DHA':     [0, 0, 0, 0, 0, 0, 0, 2299.1, 0, 0],
    '亚油酸':      [0.748, 0.49, 1.918, 0.395, 1.554, 0.475, 0.299, 0.219, 8.288, 0.752],
    '镁':          [23, 25, 15, 21, 12, 19, 20, 76, 10, 20],
    '胆碱':        [65, 80, 65, 150, 293, 290, 333, 65, 46, 64],
    '叶酸':        [6, 1, 72, 3, 47, 588, 290, 1, 1, 5],
    '泛酸':        [1.01, 0.60, 2.51, 2.25, 1.53, 6.50, 7.17, 0.86, 0.53, 1.03],
}

# ─────────────────── 三个版本的食材用量 ───────────────────
# 食材索引: 0=鸡腿, 1=猪瘦, 2=鸡心, 3=牛心, 4=蛋, 5=鸡肝, 6=牛肝, 7=鱼, 8=鸡皮, 9=鸭胸
versions = {
    'A_7%鸡皮基础版': {
        'amounts': [888, 600, 410, 445, 254, 127, 95, 127, 222, 0],
        'labels': ['鸡腿','猪瘦','鸡心','牛心','蛋','鸡肝','牛肝','鱼','鸡皮','鸭胸'],
    },
    'B_7%鸡皮+鸭胸600g': {
        'amounts': [888, 0, 410, 445, 254, 127, 95, 127, 222, 600],
        'labels': ['鸡腿','猪瘦','鸡心','牛心','蛋','鸡肝','牛肝','鱼','鸡皮','鸭胸'],
    },
    'C_鸭胸强化版': {
        'amounts': [588, 0, 410, 445, 254, 127, 95, 127, 222, 900],
        'labels': ['鸡腿','猪瘦','鸡心','牛心','蛋','鸡肝','牛肝','鱼','鸡皮','鸭胸'],
    },
}

# ─────────────────── 补充剂（三版完全相同） ───────────────────
supp = {
    '鱼油热量': 90,
    'EPA+DHA': 3000,
    '钙': 18 * 0.4004 * 1000,  # CaCO3 18g → Ca
    '铁': 1 * 36,               # 螯合铁 1粒 × 36mg
    '锌': 1 * 30,               # 锌片 1粒 × 30mg
    '锰': 1 * 10,               # 锰 1粒 × 10mg
    '碘': 7 * 225 + 3 * 25,     # 海带碘7粒 + 碘盐3g(~25mcg/g)
    '钠': 3 * 0.3934 * 1000,    # 碘盐3g → Na
    'VE': 8 * 100 * 0.6711,     # 8粒×100IU, 1IU=0.6711mg
    'VB1': 2 * 50,              # B-50 2片
    'VB2': 2 * 50,
    'VB3': 2 * 50,
    'VB6': 2 * 50,
    'VB12': 2 * 50,
    '牛磺酸': 3000,             # 牛磺酸 3g
    '氯化物': 3 * 0.6066 * 1000, # 碘盐3g → Cl
    '叶酸': 2 * 400,            # B-50 2片
    '泛酸': 2 * 50,
}

# ─────────────────── NRC 2006 RA 阈值 ───────────────────
checks = [
    ('蛋白质', 50, None, 'g'),
    ('脂肪', 22.5, None, 'g'),
    ('钙', 720, 3000, 'mg'),
    ('磷', 640, None, 'mg'),
    ('铁', 20, None, 'mg'),
    ('钾', 1300, None, 'mg'),
    ('钠', 170, None, 'mg'),
    ('锌', 18.5, None, 'mg'),
    ('铜', 1.2, None, 'mg'),
    ('锰', 1.2, None, 'mg'),
    ('碘', 350, 9000, 'mcg'),
    ('硒', 75, None, 'mcg'),
    ('牛磺酸', 250, None, 'mg'),
    ('VA', 3333, 333333, 'IU'),
    ('VD', 70, 7500, 'IU'),
    ('VE', 10, None, 'mg'),
    ('VB1', 1.4, None, 'mg'),
    ('VB2', 1.0, None, 'mg'),
    ('VB3', 10, None, 'mg'),
    ('VB6', 0.625, None, 'mg'),
    ('VB12', 5.6, None, 'mcg'),
    ('花生四烯酸', 15, None, 'mg'),
    ('EPA+DHA', 25, None, 'mg'),
    ('亚油酸', 1.4, None, 'g'),
    ('氯化物', 240, None, 'mg'),
    ('镁', 100, None, 'mg'),
    ('胆碱', 637, None, 'mg'),
    ('叶酸', 188, None, 'mcg'),
    ('泛酸', 1.44, None, 'mg'),
]

# ─────────────────── 各文档中记录的值（从文件直接抄写） ───────────────────
doc_values = {
    'A_7%鸡皮基础版': {
        'meta': {'总热量': 4809, '能量密度': 1.687, '钙磷比': 1.243},
        'nrc': {
            '蛋白质': 118.4, '脂肪': 53.9, '钙': 1577.8, '磷': 1269.8,
            '钾': 1681.3, '钠': 794.2, '氯化物': 378.4, '镁': 145.9,
            '铁': 24.0, '锌': 22.4, '铜': 3.0, '锰': 2.4,
            '碘': 382.8, '硒': 173.5, '牛磺酸': 806.9,
            'VA': 6779.7, 'VD': 250.5, 'VE': 114.6,
            'VB1': 22.5, 'VB2': 24.2, 'VB3': 56.5,
            'VB6': 23.1, 'VB12': 55.5, '胆碱': 749.6,
            '叶酸': 481.0, '泛酸': 32.0, '花生四烯酸': 595.7,
            'EPA+DHA': 1231.1, '亚油酸': 8.88,
        },
    },
    'B_7%鸡皮+鸭胸600g': {
        'meta': {'总热量': 4761, '能量密度': 1.670, '钙磷比': 1.241},
        'nrc': {
            '蛋白质': 116.0, '脂肪': 53.3, '钙': 1601.3, '磷': 1290.2,
            '钾': 1549.5, '钠': 829.9, '氯化物': 382.3, '镁': 139.8,
            '铁': 26.3, '锌': 22.6, '铜': 3.2, '锰': 2.4,
            '碘': 386.7, '硒': 151.8, '牛磺酸': 789.8,
            'VA': 6940.0, 'VD': 243.0, 'VE': 116.1,
            'VB1': 22.1, 'VB2': 24.7, 'VB3': 57.5,
            'VB6': 23.2, 'VB12': 55.8, '胆碱': 723.9,
            '叶酸': 516.1, '泛酸': 33.6, '花生四烯酸': 513.5,
            'EPA+DHA': 1243.5, '亚油酸': 9.20,
        },
    },
    'C_鸭胸强化版': {
        'meta': {'总热量': 4809, '能量密度': 1.687, '钙磷比': 1.227},
        'nrc': {
            '蛋白质': 114.1, '脂肪': 53.8, '钙': 1586.5, '磷': 1292.9,
            '钾': 1552.2, '钠': 808.5, '氯化物': 378.4, '镁': 135.9,
            '铁': 27.0, '锌': 22.5, '铜': 3.3, '锰': 2.4,
            '碘': 382.8, '硒': 144.6, '牛磺酸': 771.9,
            'VA': 6889.5, 'VD': 240.0, 'VE': 115.2,
            'VB1': 22.1, 'VB2': 24.7, 'VB3': 56.9,
            'VB6': 23.0, 'VB12': 55.2, '胆碱': 709.6,
            '叶酸': 522.8, '泛酸': 33.7, '花生四烯酸': 477.2,
            'EPA+DHA': 1231.1, '亚油酸': 9.06,
        },
    },
}

# ─────────────────── 统一总版中记录的核心结果 ───────────────────
unified_doc = {
    'A_7%鸡皮基础版': {'总热量': 4809, '能量密度': 1.687, '钙磷比': 1.243, '每日总热量': 720},
    'B_7%鸡皮+鸭胸600g': {'总热量': 4761, '能量密度': 1.670, '钙磷比': 1.241, '每日总热量': 717},
    'C_鸭胸强化版': {'总热量': 4809, '能量密度': 1.687, '钙磷比': 1.227, '每日总热量': 720},
}

# ─────────────────── 采购清单中的数据 ───────────────────
shopping_list_C = {
    '鸡腿肉_实际': 588, '鸭胸肉_实际': 900, '鸡心_实际': 410,
    '牛心_实际': 445, '鸡蛋_实际': 254, '鸡肝_实际': 127,
    '牛肝_实际': 95, '鲭鱼_实际': 127, '鸡皮_实际': 222,
    '合计': 3168, '成品': 2851, '能量密度': 1.687,
}

# ═══════════════════ 计算函数 ═══════════════════
def compute_version(name, ver):
    amounts = ver['amounts']
    raw_total = sum(amounts)
    finished = raw_total * 0.9

    # 食材贡献
    def food_total(nutrient_key):
        arr = nut[nutrient_key]
        return sum(a / 100 * arr[i] for i, a in enumerate(amounts))

    food = {k: food_total(k) for k in nut}
    kcal = food['能量'] + supp['鱼油热量']
    density = kcal / finished if finished > 0 else 0
    per1k = lambda x: x / kcal * 1000

    final = {
        '蛋白质': food['蛋白质'],
        '脂肪': food['脂肪'],
        '钙': food['钙'] + supp['钙'],
        '磷': food['磷'],
        '铁': food['铁'] + supp['铁'],
        '锌': food['锌'] + supp['锌'],
        '铜': food['铜'],
        '锰': food['锰'] + supp['锰'],
        '钾': food['钾'],
        '钠': food['钠'] + supp['钠'],
        '碘': food['碘'] + supp['碘'],
        '硒': food['硒'],
        '牛磺酸': food['牛磺酸'] * 0.4 + supp['牛磺酸'],
        'VA': food['VA'],
        'VD': food['VD'],
        'VE': food['VE'] + supp['VE'],
        'VB1': food['VB1'] + supp['VB1'],
        'VB2': food['VB2'] + supp['VB2'],
        'VB3': food['VB3'] + supp['VB3'],
        'VB6': food['VB6'] + supp['VB6'],
        'VB12': food['VB12'] + supp['VB12'],
        '花生四烯酸': food['花生四烯酸'],
        'EPA+DHA': food['EPA+DHA'] + supp['EPA+DHA'],
        '亚油酸': food['亚油酸'],
        '氯化物': supp['氯化物'],
        '镁': food['镁'],
        '胆碱': food['胆碱'],
        '叶酸': food['叶酸'] + supp['叶酸'],
        '泛酸': food['泛酸'] + supp['泛酸'],
    }

    ca_p = final['钙'] / final['磷'] if final['磷'] > 0 else 0

    # NRC 验证
    nrc_results = {}
    nrc_pass = 0
    nrc_fail = 0
    for nname, low, high, unit in checks:
        value = per1k(final[nname])
        ok = value >= low and (high is None or value <= high)
        nrc_results[nname] = value
        if ok:
            nrc_pass += 1
        else:
            nrc_fail += 1

    # 每日热量
    catfood_kcal_per_g = density
    cat_a = 30 * 4.0 + 60 * catfood_kcal_per_g
    cat_b = 30 * 4.0 + 50 * catfood_kcal_per_g
    cat_c = 40 * 4.0 + 80 * catfood_kcal_per_g

    return {
        'raw_total': raw_total,
        'finished': finished,
        'kcal': kcal,
        'density': density,
        'ca_p': ca_p,
        'nrc': nrc_results,
        'nrc_pass': nrc_pass,
        'nrc_fail': nrc_fail,
        'cat_a': cat_a,
        'cat_b': cat_b,
        'cat_c': cat_c,
        'daily_total': cat_a + cat_b + cat_c,
    }


# ═══════════════════ 主检查 ═══════════════════
all_issues = []

for vname, ver in versions.items():
    print('=' * 72)
    print(f'>>> 版本: {vname}')
    print('=' * 72)

    result = compute_version(vname, ver)

    print(f'原料总量: {result["raw_total"]}g')
    print(f'成品重量: {result["finished"]:.1f}g')
    print(f'总能量: {result["kcal"]:.1f} kcal')
    print(f'能量密度: {result["density"]:.3f} kcal/g')
    print(f'Ca:P = {result["ca_p"]:.3f}')
    print(f'NRC通过: {result["nrc_pass"]}/29')
    print(f'日热量: A={result["cat_a"]:.1f}, B={result["cat_b"]:.1f}, C={result["cat_c"]:.1f}, 合计={result["daily_total"]:.1f}')
    print()

    # ── 检查NRC是否真的29/29 ──
    if result['nrc_fail'] > 0:
        msg = f'{vname}: NRC 验证失败 {result["nrc_fail"]} 项！'
        all_issues.append(('严重', msg))
        print(f'⚠️  {msg}')

    # ── 与单独版本文档对比 ──
    if vname in doc_values:
        dv = doc_values[vname]
        # meta
        doc_kcal = dv['meta']['总热量']
        doc_density = dv['meta']['能量密度']
        doc_cap = dv['meta']['钙磷比']
        if abs(result['kcal'] - doc_kcal) > 5:
            msg = f'{vname}: 总热量 计算={result["kcal"]:.1f} 文档={doc_kcal}'
            all_issues.append(('数据偏差', msg))
        if abs(result['density'] - doc_density) > 0.005:
            msg = f'{vname}: 能量密度 计算={result["density"]:.3f} 文档={doc_density}'
            all_issues.append(('数据偏差', msg))
        if abs(result['ca_p'] - doc_cap) > 0.005:
            msg = f'{vname}: Ca:P 计算={result["ca_p"]:.3f} 文档={doc_cap}'
            all_issues.append(('数据偏差', msg))

        # nrc per 1000kcal
        print(f'{"营养素":<10} {"计算值":>12} {"文档值":>12} {"偏差":>10}  状态')
        print('-' * 60)
        for nname in dv['nrc']:
            calc = result['nrc'][nname]
            doc = dv['nrc'][nname]
            diff = calc - doc
            pct = abs(diff / doc * 100) if doc != 0 else 0
            status = '✅' if pct < 2.0 else ('⚠️' if pct < 5.0 else '❌')
            if pct >= 2.0:
                msg = f'{vname}: {nname} 计算={calc:.2f} 文档={doc} 偏差={pct:.1f}%'
                all_issues.append(('NRC偏差', msg))
            print(f'{nname:<10} {calc:>12.2f} {doc:>12.1f} {diff:>+10.2f}  {status}')
        print()

    # ── 与统一总版对比 ──
    if vname in unified_doc:
        ud = unified_doc[vname]
        if abs(result['kcal'] - ud['总热量']) > 5:
            msg = f'{vname}: 统一总版-总热量 计算={result["kcal"]:.1f} 文档={ud["总热量"]}'
            all_issues.append(('统一总版偏差', msg))
        if abs(result['density'] - ud['能量密度']) > 0.005:
            msg = f'{vname}: 统一总版-能量密度 计算={result["density"]:.3f} 文档={ud["能量密度"]}'
            all_issues.append(('统一总版偏差', msg))
        if abs(result['ca_p'] - ud['钙磷比']) > 0.005:
            msg = f'{vname}: 统一总版-Ca:P 计算={result["ca_p"]:.3f} 文档={ud["钙磷比"]}'
            all_issues.append(('统一总版偏差', msg))

# ── 采购清单与C版交叉校验 ──
print('=' * 72)
print('>>> 采购清单(鸭胸强化版) vs C版配方 交叉校验')
print('=' * 72)
c_amounts = versions['C_鸭胸强化版']['amounts']
sl_checks = [
    ('鸡腿肉', c_amounts[0], shopping_list_C['鸡腿肉_实际']),
    ('鸭胸肉', c_amounts[9], shopping_list_C['鸭胸肉_实际']),
    ('鸡心',   c_amounts[2], shopping_list_C['鸡心_实际']),
    ('牛心',   c_amounts[3], shopping_list_C['牛心_实际']),
    ('鸡蛋',   c_amounts[4], shopping_list_C['鸡蛋_实际']),
    ('鸡肝',   c_amounts[5], shopping_list_C['鸡肝_实际']),
    ('牛肝',   c_amounts[6], shopping_list_C['牛肝_实际']),
    ('鲭鱼',   c_amounts[7], shopping_list_C['鲭鱼_实际']),
    ('鸡皮',   c_amounts[8], shopping_list_C['鸡皮_实际']),
]
for item, expected, actual in sl_checks:
    status = '✅' if expected == actual else '❌'
    if expected != actual:
        msg = f'采购清单: {item} 配方={expected}g 清单={actual}g'
        all_issues.append(('采购清单偏差', msg))
    print(f'{item}: 配方={expected}g  清单={actual}g  {status}')

c_result = compute_version('C_鸭胸强化版', versions['C_鸭胸强化版'])
if abs(c_result['density'] - shopping_list_C['能量密度']) > 0.005:
    msg = f'采购清单: 能量密度 计算={c_result["density"]:.3f} 清单={shopping_list_C["能量密度"]}'
    all_issues.append(('采购清单偏差', msg))

# ── 版本间比例一致性检查 ──
print()
print('=' * 72)
print('>>> 配方比例一致性检查（文档中声称的百分比 vs 实际克数）')
print('=' * 72)

# A版: 鸡腿28%, 猪瘦19%, 鸡心13%, 牛心14%, 蛋8%, 鸡肝4%, 牛肝3%, 鱼4%, 皮7%
# B版: 鸡腿28%, 鸭胸19%, 鸡心13%, 牛心14%, 蛋8%, 鸡肝4%, 牛肝3%, 鱼4%, 皮7%
# C版: 鸡腿19%, 鸭胸28%, 鸡心13%, 牛心14%, 蛋8%, 鸡肝4%, 牛肝3%, 鱼4%, 皮7%

pct_claims = {
    'A_7%鸡皮基础版': [28, 19, 13, 14, 8, 4, 3, 4, 7, 0],
    'B_7%鸡皮+鸭胸600g': [28, 0, 13, 14, 8, 4, 3, 4, 7, 19],
    'C_鸭胸强化版': [19, 0, 13, 14, 8, 4, 3, 4, 7, 28],
}

ingredient_names = ['鸡腿','猪瘦','鸡心','牛心','蛋','鸡肝','牛肝','鱼','鸡皮','鸭胸']

for vname in versions:
    amounts = versions[vname]['amounts']
    raw_total = sum(amounts)
    claimed = pct_claims[vname]
    print(f'\n{vname} (总量={raw_total}g):')
    for i, (ing, amt, pct) in enumerate(zip(ingredient_names, amounts, claimed)):
        if amt == 0 and pct == 0:
            continue
        actual_pct = amt / raw_total * 100
        expected_g = pct / 100 * raw_total
        diff = abs(actual_pct - pct)
        status = '✅' if diff < 1.0 else '⚠️'
        if diff >= 1.0:
            msg = f'{vname}: {ing} 声称={pct}% 实际={actual_pct:.1f}% ({amt}g/{raw_total}g)'
            all_issues.append(('比例偏差', msg))
        print(f'  {ing}: 声称{pct}%={expected_g:.0f}g, 实际={amt}g ({actual_pct:.1f}%)  {status}')

# ── B版每日分配热量检验 ──
print()
print('=' * 72)
print('>>> 每日分配热量检验')
print('=' * 72)

for vname in versions:
    r = compute_version(vname, versions[vname])
    d = r['density']
    doc_daily = doc_values[vname]['meta'].get('总热量', 0)
    a_kcal = 30 * 4.0 + 60 * d
    b_kcal = 30 * 4.0 + 50 * d
    c_kcal = 40 * 4.0 + 80 * d
    print(f'{vname}: 密度={d:.3f}, A={a_kcal:.1f}, B={b_kcal:.1f}, C={c_kcal:.1f}, 合计={a_kcal+b_kcal+c_kcal:.1f}')

# ═══════════════════ 最终汇总 ═══════════════════
print()
print('=' * 72)
print('>>> 最终汇总')
print('=' * 72)

if not all_issues:
    print('✅ 所有检查全部通过，文档之间完全一致！')
else:
    print(f'共发现 {len(all_issues)} 处需要关注的问题：')
    for severity, msg in all_issues:
        print(f'  [{severity}] {msg}')
