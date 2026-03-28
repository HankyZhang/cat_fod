# -*- coding: utf-8 -*-
"""
完整重新验证脚本
1. 检查代码数组 vs 文档实际配方是否一致
2. 用文档的实际配方重新计算全部29项NRC
3. 验证鸡皮替换问题
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================
# 食材营养数据 (per 100g raw)
# 顺序: [鸡腿, 猪瘦肉, 鸡心, 牛心, 鸡蛋, 鸡肝, 牛肝, 鲅鱼, 鸡皮, 鸭胸]
# ============================================================
names = ['鸡腿', '猪瘦肉', '鸡心', '牛心', '鸡蛋', '鸡肝', '牛肝', '鲅鱼', '鸡皮', '鸭胸']

spanish = {
    '能量': 139, '蛋白质': 19.29, '脂肪': 6.30,
    '磷': 171, '钙': 11, '铁': 0.44, '锌': 0.51, '铜': 0.046, '锰': 0.015,
    '钾': 446, '钠': 59, '碘': 35, '硒': 36.5,
    'VA': 98, 'VD': 16, 'VE': 0.42,
    'VB1': 0.068, 'VB2': 0.130, 'VB3': 8.47, 'VB6': 0.315, 'VB12': 7.4,
    '牛磺酸': 70, '花生四烯酸': 60, 'EPA+DHA': 941, '亚油酸': 0.100,
    '镁': 33, '胆碱': 65, '叶酸': 2, '泛酸': 0.42,
}

nut = {
    '能量':        [119, 143, 153, 112, 143, 119, 135, spanish['能量'],   349, 135],
    '蛋白质':      [19.6, 21.1, 15.6, 17.7, 12.6, 16.9, 20.4, spanish['蛋白质'], 13.3, 18.28],
    '脂肪':        [4.3, 6.9, 9.3, 3.9, 9.9, 4.8, 3.6, spanish['脂肪'], 32.4, 5.95],
    '磷':          [178, 197, 177, 212, 198, 297, 387, spanish['磷'],   68, 203],
    '钙':          [9, 5, 12, 7, 56, 8, 5, spanish['钙'],     11, 11],
    '铁':          [0.8, 0.8, 5.9, 4.3, 1.8, 9.0, 4.9, spanish['铁'],   0.7, 2.4],
    '锌':          [1.8, 1.9, 6.6, 2.4, 1.3, 2.7, 4.0, spanish['锌'],   0.6, 1.9],
    '铜':          [0.06, 0.06, 0.33, 0.39, 0.07, 0.49, 9.76, spanish['铜'], 0.02, 0.24],
    '锰':          [0.02, 0.01, 0.05, 0.03, 0.03, 0.26, 0.31, spanish['锰'], 0.01, 0.02],
    '钾':          [242.0, 389.0, 176.066, 286.984, 138.0, 230.0, 313.0, spanish['钾'], 119.0, 271.0],
    '钠':          [95.0, 52.0, 73.934, 97.989, 142.0, 71.0, 69.0, spanish['钠'], 51.0, 74.0],
    '碘':          [1, 1, 5, 5, 27, 3, 3, spanish['碘'],     1, 1],
    '硒':          [23.0, 32.5, 16.0, 21.8, 30.7, 54.6, 39.7, spanish['硒'], 14.1, 14.0],
    'VA':          [50, 7, 31, 0, 520, 11078, 16898, spanish['VA'],   150, 24],
    'VD':          [5, 12, 0, 0, 82, 12, 49, spanish['VD'],   0, 0],
    'VE':          [0.2, 0.5, 0.7, 0.2, 1.1, 0.7, 0.5, spanish['VE'], 0.3, 0.7],
    'VB1':         [0.07, 0.81, 0.13, 0.24, 0.04, 0.31, 0.19, spanish['VB1'], 0.01, 0.36],
    'VB2':         [0.16, 0.23, 0.73, 0.91, 0.46, 1.78, 2.76, spanish['VB2'], 0.07, 0.47],
    'VB3':         [5.3, 5.0, 4.8, 7.4, 0.1, 9.7, 13.2, spanish['VB3'], 2.5, 5.3],
    'VB6':         [0.33, 0.42, 0.29, 0.28, 0.14, 0.85, 1.08, spanish['VB6'], 0.05, 0.34],
    'VB12':        [0.4, 0.6, 7.3, 8.6, 0.9, 16.6, 59.3, spanish['VB12'], 0.3, 0.4],
    '牛磺酸':      [40, 50, 145, 160, 20, 30, 40, spanish['牛磺酸'], 10, 0],
    '花生四烯酸':  [50, 70, 84, 25, 155, 260, 200, spanish['花生四烯酸'], 250, 0],
    'EPA+DHA':     [0, 0, 0, 0, 0, 0, 0, spanish['EPA+DHA'], 0, 0],
    '亚油酸':      [0.748, 0.49, 1.918, 0.395, 1.554, 0.475, 0.299, spanish['亚油酸'], 8.288, 0.752],
    '镁':          [23, 25, 15, 21, 12, 19, 20, spanish['镁'],   10, 20],
    '胆碱':        [65, 80, 65, 150, 293, 290, 333, spanish['胆碱'], 46, 64],
    '叶酸':        [6, 1, 72, 3, 47, 588, 290, spanish['叶酸'], 1, 5],
    '泛酸':        [1.01, 0.60, 2.51, 2.25, 1.53, 6.50, 7.17, spanish['泛酸'], 0.53, 1.03],
}

# ============================================================
# 补充剂明细 — 逐项分解
# ============================================================
print("=" * 80)
print("第一部分：补充剂逐项分解验证")
print("=" * 80)

supp_detail = {
    '碳酸钙 18g':    {'钙': 18 * 0.4004 * 1000},          # 7207mg
    '鱼油 10粒':     {'EPA+DHA': 10 * 300, '热量': 90},    # 3000mg, 90kcal
    'VD3 1粒':       {'VD': 1000},                          # 1000IU
    'VE 8粒×100IU':  {'VE': 8 * 100 * 0.6711},             # 536.9mg
    'B-50 2片': {
        'VB1': 2 * 50,     # 100mg
        'VB2': 2 * 50,     # 100mg
        'VB3': 2 * 50,     # 100mg
        'VB6': 2 * 50,     # 100mg
        'VB12': 2 * 50,    # 100mcg
        '叶酸': 2 * 400,   # 800mcg
        '泛酸': 2 * 50,    # 100mg
    },
    '海带碘 7粒':    {'碘': 7 * 225},                       # 1575mcg
    '碘盐 3g':       {'碘': 3 * 25, '钠': 3*0.3934*1000, '氯化物': 3*0.6066*1000},
    '锌片 1粒':      {'锌': 30},                            # 30mg
    '螯合铁 1粒':    {'铁': 36},                            # 36mg
    '锰片 1粒':      {'锰': 10},                            # 10mg
    '牛磺酸 3g':     {'牛磺酸': 3000},                      # 3000mg
}

for name, vals in supp_detail.items():
    parts = [f"{k}={v:.1f}" for k,v in vals.items()]
    print(f"  {name:<20} → {', '.join(parts)}")

# 汇总补充剂
supp_total = {}
for name, vals in supp_detail.items():
    for k, v in vals.items():
        supp_total[k] = supp_total.get(k, 0) + v

print(f"\n补充剂汇总:")
for k, v in supp_total.items():
    unit = 'IU' if k in ['VA','VD'] else ('mcg' if k in ['碘','VB12','叶酸','硒'] else ('kcal' if k=='热量' else 'mg'))
    print(f"  {k}: {v:.1f} {unit}")

# ============================================================
# 第二部分：代码数组 vs 文档配方 对比
# ============================================================
print("\n" + "=" * 80)
print("第二部分：代码数组 vs 文档实际配方 对比")
print("=" * 80)

# 代码中的数组 (来自 calc_all_spanish_versions.py)
code_versions = {
    'A_代码': [888, 600, 410, 445, 254, 127, 95, 127, 222, 0],
    'B_代码': [888, 0, 410, 445, 254, 127, 95, 127, 222, 600],
    'C_代码': [588, 0, 410, 445, 254, 127, 95, 127, 222, 900],
}

# 文档中写的配方
doc_versions = {
    'A_文档': [888, 600, 410, 445, 254, 127, 95, 127, 222, 0],
    'B_文档': [288, 600, 410, 445, 254, 127, 95, 127, 222, 600],
    'C_文档': [0, 600, 410, 445, 254, 127, 95, 127, 222, 900],
}

for ver_name in ['A', 'B', 'C']:
    code_key = f'{ver_name}_代码'
    doc_key = f'{ver_name}_文档'
    code_arr = code_versions[code_key]
    doc_arr = doc_versions[doc_key]
    
    match = "✅ 完全一致" if code_arr == doc_arr else "❌ 不一致!"
    print(f"\n{ver_name}版: {match}")
    print(f"  代码总量: {sum(code_arr)}g")
    print(f"  文档总量: {sum(doc_arr)}g")
    
    if code_arr != doc_arr:
        print(f"  差异详情:")
        for i, name in enumerate(names):
            if code_arr[i] != doc_arr[i]:
                print(f"    {name}: 代码={code_arr[i]}g, 文档={doc_arr[i]}g")

# ============================================================
# 第三部分：用文档配方重新计算全部29项NRC
# ============================================================
print("\n" + "=" * 80)
print("第三部分：分别用代码数组和文档配方计算NRC，对比差异")
print("=" * 80)

# NRC 2006 成猫 RA
nrc_checks = [
    ("蛋白质",      50,     None,    '蛋白质',      "g"),
    ("脂肪",        22.5,   None,    '脂肪',        "g"),
    ("钙",          720,    3000,    '钙',          "mg"),
    ("磷",          640,    None,    '磷',          "mg"),
    ("铁",          20,     None,    '铁',          "mg"),
    ("锌",          18.5,   None,    '锌',          "mg"),
    ("铜",          1.2,    None,    '铜',          "mg"),
    ("锰",          1.2,    None,    '锰',          "mg"),
    ("碘",          350,    9000,    '碘',          "mcg"),
    ("硒",          75,     None,    '硒',          "mcg"),
    ("维生素A",     3333,   333333,  'VA',          "IU"),
    ("维生素D",     70,     7500,    'VD',          "IU"),
    ("维生素E",     10,     None,    'VE',          "mg"),
    ("维生素B1",    1.4,    None,    'VB1',         "mg"),
    ("维生素B2",    1.0,    None,    'VB2',         "mg"),
    ("维生素B3",    10,     None,    'VB3',         "mg"),
    ("维生素B6",    0.625,  None,    'VB6',         "mg"),
    ("维生素B12",   5.6,    None,    'VB12',        "mcg"),
    ("牛磺酸",      250,    None,    '牛磺酸',      "mg"),
    ("花生四烯酸",  15,     None,    '花生四烯酸',  "mg"),
    ("EPA+DHA",     25,     None,    'EPA+DHA',     "mg"),
    ("亚油酸",      1.4,    None,    '亚油酸',      "g"),
    ("氯化物",      240,    None,    '氯化物',      "mg"),
    ("镁",          12,     None,    '镁',          "mg"),
    ("胆碱",        50,     None,    '胆碱',        "mg"),
    ("叶酸",        188,    None,    '叶酸',        "mcg"),
    ("泛酸",        1.44,   None,    '泛酸',        "mg"),
    ("钾",          130,    None,    '钾',          "mg"),
    ("钠",          170,    None,    '钠',          "mg"),
]

def calc_version(amounts, label):
    """对给定食材数组计算完整NRC校验"""
    def food_total(key):
        return sum(amounts[i] / 100 * nut[key][i] for i in range(10))
    
    food = {k: food_total(k) for k in nut}
    
    # 补充剂
    fish_oil_kcal = 90
    kcal = food['能量'] + fish_oil_kcal
    raw_total = sum(amounts)
    finished = raw_total * 0.9
    density = kcal / finished
    
    final = {
        '蛋白质': food['蛋白质'],
        '脂肪': food['脂肪'],
        '钙': food['钙'] + supp_total.get('钙', 0),
        '磷': food['磷'],
        '铁': food['铁'] + supp_total.get('铁', 0),
        '锌': food['锌'] + supp_total.get('锌', 0),
        '铜': food['铜'],
        '锰': food['锰'] + supp_total.get('锰', 0),
        '钾': food['钾'],
        '钠': food['钠'] + supp_total.get('钠', 0),
        '碘': food['碘'] + supp_total.get('碘', 0),
        '硒': food['硒'],
        '牛磺酸': food['牛磺酸'] * 0.4 + supp_total.get('牛磺酸', 0),
        'VA': food['VA'],
        'VD': food['VD'] + supp_total.get('VD', 0),
        'VE': food['VE'] + supp_total.get('VE', 0),
        'VB1': food['VB1'] + supp_total.get('VB1', 0),
        'VB2': food['VB2'] + supp_total.get('VB2', 0),
        'VB3': food['VB3'] + supp_total.get('VB3', 0),
        'VB6': food['VB6'] + supp_total.get('VB6', 0),
        'VB12': food['VB12'] + supp_total.get('VB12', 0),
        '花生四烯酸': food['花生四烯酸'],
        'EPA+DHA': food['EPA+DHA'] + supp_total.get('EPA+DHA', 0),
        '亚油酸': food['亚油酸'],
        '氯化物': supp_total.get('氯化物', 0),
        '镁': food['镁'],
        '胆碱': food['胆碱'],
        '叶酸': food['叶酸'] + supp_total.get('叶酸', 0),
        '泛酸': food['泛酸'] + supp_total.get('泛酸', 0),
    }
    
    per1k = lambda x: x / kcal * 1000
    ca_p = final['钙'] / final['磷']
    
    pass_count = 0
    fail_items = []
    results = {}
    
    for lbl, nrc_min, nrc_max, key, unit in nrc_checks:
        val_p1k = per1k(final[key])
        results[lbl] = val_p1k
        ok = True
        if val_p1k < nrc_min:
            ok = False
            fail_items.append((lbl, val_p1k, nrc_min, unit))
        if nrc_max and val_p1k > nrc_max:
            ok = False
            fail_items.append((lbl, val_p1k, nrc_max, unit))
        if ok:
            pass_count += 1
    
    return {
        'kcal': kcal, 'density': density, 'ca_p': ca_p,
        'pass': pass_count, 'total': len(nrc_checks),
        'fails': fail_items, 'results': results, 'final': final,
        'food': food, 'raw': raw_total, 'finished': finished,
    }

# 计算所有版本
all_results = {}
for ver_name, amounts in {**code_versions, **doc_versions}.items():
    all_results[ver_name] = calc_version(amounts, ver_name)

# 输出对比
for ver in ['A', 'B', 'C']:
    code_r = all_results[f'{ver}_代码']
    doc_r = all_results[f'{ver}_文档']
    
    print(f"\n{'─' * 80}")
    print(f"  {ver}版对比: 代码 vs 文档")
    print(f"{'─' * 80}")
    print(f"  {'':>14} {'代码':>12} {'文档':>12} {'差异':>10}")
    print(f"  {'总热量':>14} {code_r['kcal']:>10.1f}  {doc_r['kcal']:>10.1f}  {doc_r['kcal']-code_r['kcal']:>+10.1f}")
    print(f"  {'能量密度':>14} {code_r['density']:>10.3f}  {doc_r['density']:>10.3f}  {doc_r['density']-code_r['density']:>+10.3f}")
    print(f"  {'Ca:P':>14} {code_r['ca_p']:>10.3f}  {doc_r['ca_p']:>10.3f}  {doc_r['ca_p']-code_r['ca_p']:>+10.3f}")
    print(f"  {'NRC通过':>14} {code_r['pass']:>10}/{code_r['total']}  {doc_r['pass']:>10}/{doc_r['total']}")
    
    # 逐项对比差异大的
    diffs = []
    for lbl, nrc_min, nrc_max, key, unit in nrc_checks:
        cv = code_r['results'][lbl]
        dv = doc_r['results'][lbl]
        if abs(cv - dv) > 0.5:  # 差异>0.5的才显示
            diffs.append((lbl, cv, dv, dv-cv, unit, nrc_min))
    
    if diffs:
        print(f"\n  营养素差异 (>0.5):")
        print(f"  {'营养素':<12} {'代码/1000kcal':>14} {'文档/1000kcal':>14} {'差异':>10} {'NRC最低':>10}")
        for lbl, cv, dv, diff, unit, nrc_min in diffs:
            print(f"  {lbl:<12} {cv:>12.1f}  {dv:>12.1f}  {diff:>+10.1f} {nrc_min:>10}")
    
    if doc_r['fails']:
        print(f"\n  文档版不达标项:")
        for lbl, val, target, unit in doc_r['fails']:
            print(f"    ❌ {lbl}: {val:.1f} vs NRC {target} {unit}/1000kcal")

# ============================================================
# 第四部分：C版文档配方详细NRC校验（推荐版）
# ============================================================
print("\n" + "=" * 80)
print("第四部分：C版(文档配方)完整NRC校验")
print("配方: 鸭胸900, 鸡腿0, 猪瘦肉600, 鸡心410, 牛心445, 蛋254, 鸡肝127, 牛肝95, 鲅鱼127, 鸡皮222")
print("=" * 80)

c_doc = all_results['C_文档']
print(f"\n原料总量: {c_doc['raw']}g → 成品: {c_doc['finished']:.0f}g")
print(f"总热量: {c_doc['kcal']:.1f} kcal")
print(f"能量密度: {c_doc['density']:.3f} kcal/g")
print(f"Ca:P = {c_doc['ca_p']:.3f}")

print(f"\n{'营养素':<12} {'每1000kcal':>12} {'NRC最低':>10} {'NRC上限':>10} {'状态':>6}")
print("-" * 58)

for lbl, nrc_min, nrc_max, key, unit in nrc_checks:
    val = c_doc['results'][lbl]
    status = "✅"
    if val < nrc_min:
        status = "❌"
    elif nrc_max and val > nrc_max:
        status = "⚠️超"
    nmax = f"{nrc_max}" if nrc_max else "—"
    print(f"{lbl:<12} {val:>10.1f}{unit:<4} {nrc_min:>10} {nmax:>10} {status}")

print(f"\n结果: {c_doc['pass']}/{c_doc['total']} 通过")

# ============================================================
# 第五部分：鸡皮替换分析
# ============================================================
print("\n" + "=" * 80)
print("第五部分：鸡皮 vs 鸡腿 营养对比 & 替换分析")
print("=" * 80)

print(f"\n每100g营养对比:")
print(f"{'指标':<12} {'鸡皮':>8} {'鸡腿':>8} {'差异':>10}")
print("-" * 42)
compare_keys = ['能量', '蛋白质', '脂肪', '铁', '锌', 'VA', 'VD', '亚油酸']
for k in compare_keys:
    skin = nut[k][8]  # 鸡皮 index=8
    thigh = nut[k][0] # 鸡腿 index=0
    unit = 'kcal' if k=='能量' else ('g' if k in ['蛋白质','脂肪','亚油酸'] else ('IU' if k in ['VA','VD'] else 'mg'))
    print(f"{k:<12} {skin:>8.1f} {thigh:>8.1f} {skin-thigh:>+10.1f} {unit}")

# 测试: C版文档配方,鸡皮从222g减到100g,多出来的加到鸡腿
# C_文档: [0, 600, 410, 445, 254, 127, 95, 127, 222, 900]
skin_short = 122  # 少了122g鸡皮
c_skin_low = [0 + skin_short, 600, 410, 445, 254, 127, 95, 127, 222-skin_short, 900]
c_skin_result = calc_version(c_skin_low, "C_鸡皮不足_替换为鸡腿")

print(f"\n模拟: 鸡皮只有100g（少122g），用鸡腿补足：")
print(f"  原方案: 鸡腿0 + 鸡皮222g")
print(f"  新方案: 鸡腿122g + 鸡皮100g")
print(f"\n  NRC: {c_skin_result['pass']}/{c_skin_result['total']} 通过")
print(f"  热量: {c_doc['kcal']:.1f} → {c_skin_result['kcal']:.1f} kcal ({c_skin_result['kcal']-c_doc['kcal']:+.1f})")
print(f"  脂肪/1000kcal: {c_doc['results']['脂肪']:.1f} → {c_skin_result['results']['脂肪']:.1f}g")
print(f"  蛋白/1000kcal: {c_doc['results']['蛋白质']:.1f} → {c_skin_result['results']['蛋白质']:.1f}g")
print(f"  Ca:P: {c_doc['ca_p']:.3f} → {c_skin_result['ca_p']:.3f}")

if c_skin_result['fails']:
    print(f"  不达标项:")
    for lbl, val, target, unit in c_skin_result['fails']:
        print(f"    ❌ {lbl}: {val:.1f} vs NRC {target}")
else:
    print(f"  ✅ 全部达标!")

# 测试: 完全没鸡皮
c_no_skin = [222, 600, 410, 445, 254, 127, 95, 127, 0, 900]
c_no_skin_result = calc_version(c_no_skin, "C_无鸡皮_全部换鸡腿")
print(f"\n模拟: 完全没鸡皮（222g全部换成鸡腿）：")
print(f"  NRC: {c_no_skin_result['pass']}/{c_no_skin_result['total']} 通过")
print(f"  热量: {c_doc['kcal']:.1f} → {c_no_skin_result['kcal']:.1f} kcal ({c_no_skin_result['kcal']-c_doc['kcal']:+.1f})")
print(f"  脂肪/1000kcal: {c_doc['results']['脂肪']:.1f} → {c_no_skin_result['results']['脂肪']:.1f}g")
if c_no_skin_result['fails']:
    for lbl, val, target, unit in c_no_skin_result['fails']:
        print(f"  ❌ {lbl}: {val:.1f} vs NRC {target}")
else:
    print(f"  ✅ 全部达标!")

# ============================================================
# 第六部分：文档需要修正的地方
# ============================================================
print("\n" + "=" * 80)
print("第六部分：文档 vs 代码 差异总结")
print("=" * 80)

print("""
A版: ✅ 代码和文档一致, 无需修改

B版: ❌ 代码和文档不一致
  - 代码: 鸡腿=888g, 猪瘦肉=0g, 鸭胸=600g (总量3168)
  - 文档: 鸡腿=288g, 猪瘦肉=600g, 鸭胸=600g (总量3168)
  - 差异: 代码把猪瘦肉600g并入了鸡腿(888=288+600)
  - 影响: 鸡腿(VB1=0.07)远低于猪瘦肉(VB1=0.81), 其他差异也有

C版: ❌ 代码和文档不一致  
  - 代码: 鸡腿=588g, 猪瘦肉=0g, 鸭胸=900g (总量3168)
  - 文档: 鸡腿=0g, 猪瘦肉=600g, 鸭胸=900g (总量3180)
  - 差异: 代码用鸡腿588g代替了猪瘦肉600g, 且总量差12g
  - 影响: 类似B版

结论: 文档配方和代码验证的不是同一个配方!
需要决定: 以文档为准还是以代码为准?
→ 建议: 以文档为准(因为用户按文档采购), 重新验证文档版是否通过29/29
""")
