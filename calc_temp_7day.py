# -*- coding: utf-8 -*-
"""
临时7天版计算脚本
——补充剂到4月8日才到，现有：碳酸钙、牛磺酸、锰、碘化钾、恒健VB、双鲸VE
——缺少：鱼油、VD3、锌片、螯合铁、B-50、海带碘
基于C版(鸭胸强化版)等比缩小
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================
# 食材营养数据 (per 100g raw)
# 顺序: [鸡腿, 猪瘦肉, 鸡心, 牛心, 鸡蛋, 鸡肝, 牛肝, 鲅鱼, 鸡皮, 鸭胸]
# ============================================================
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

names = ['鸡腿', '猪瘦肉', '鸡心', '牛心', '鸡蛋', '鸡肝', '牛肝', '鲅鱼', '鸡皮', '鸭胸']

# ============================================================
# 7天配方 — 基于C版验证数组等比缩小 (7/15)
# C版15天验证数组: [588, 0, 410, 445, 254, 127, 95, 127, 222, 900] = 3168g
# 用户实操: 鸡腿588g位置可用猪瘦肉替代(营养接近)
# ============================================================

amounts_7d = [
    274,   # 鸡腿 (588*7/15=274.4) — 实操中可用280g猪瘦肉替代
    0,     # 猪瘦肉 (代码版本此位=0)
    191,   # 鸡心 (410*7/15=191.3)
    208,   # 牛心 (445*7/15=207.7)
    119,   # 鸡蛋 (254*7/15=118.5 ≈ 2个大蛋)
    59,    # 鸡肝 (127*7/15=59.3)
    44,    # 牛肝 (95*7/15=44.3)
    59,    # 鲅鱼 (127*7/15=59.3)
    104,   # 鸡皮 (222*7/15=103.6)
    420,   # 鸭胸 (900*7/15=420)
]

raw_total = sum(amounts_7d)
finished = raw_total * 0.90

print("=" * 72)
print("临时7天版 — 仅用现有补充剂 (基于C版鸭胸强化版)")
print("=" * 72)
print(f"\n原料总量: {raw_total}g → 成品: {finished:.0f}g (出成率90%)")
print(f"\n{'食材':<16} {'用量(g)':>8}")
print("-" * 28)
for i, name in enumerate(names):
    if amounts_7d[i] > 0:
        print(f"{name:<16} {amounts_7d[i]:>8}g")
print(f"{'合计':<16} {raw_total:>8}g")

# ============================================================
# 补充剂 — 仅现有
# ============================================================
# 恒健VB典型规格 (每片, 中国国标日推荐量水平)
hengjian = {'VB1': 1.4, 'VB2': 1.4, 'VB3': 16.0, 'VB5': 6.0, 'VB6': 1.4, 'VB12': 2.4, '叶酸': 400}
hengjian_tabs = 2

supp_desc = {
    '碳酸钙粉': '8g (→ Ca 3203mg)',
    '牛磺酸粉': '1.5g (分批: 1g入锅 + 0.5g每日现加)',
    '锰片 10mg': '1粒',
    '双鲸VE 100IU': '4粒 (→ 268mg)',
    '恒健VB': f'{hengjian_tabs}片',
    '碘盐': '1.5g (补钠+氯化物+少量碘)',
    '碘化钾': '见下方计算',
}

print("\n" + "=" * 72)
print("现有补充剂")
print("=" * 72)
for name, desc in supp_desc.items():
    print(f"  ✅ {name}: {desc}")
print("\n  ❌ 缺少: 鱼油, VD3 1000IU, 锌片, 螯合铁, NOW B-50, 海带碘")

# ============================================================
# 计算总营养
# ============================================================
def food_total(key):
    return sum(amounts_7d[i] / 100 * nut[key][i] for i in range(10))

food = {k: food_total(k) for k in nut}
kcal = food['能量']  # 无鱼油
per1k = lambda x: x / kcal * 1000
density = kcal / finished

# 碘补充计算
iodine_nrc_min = 350  # mcg/1000kcal
iodine_food = food['碘']
iodine_salt = 1.5 * 25  # 碘盐1.5g, 保守25mcg/g
iodine_current = iodine_food + iodine_salt
iodine_need_total = iodine_nrc_min * kcal / 1000
iodine_deficit = max(0, iodine_need_total - iodine_current)
# KI→I: 76.4% (126.9/166.0)
ki_needed_mcg = iodine_deficit / 0.764
ki_needed_mg = ki_needed_mcg / 1000

# 最终营养值
final = {
    '蛋白质': food['蛋白质'],
    '脂肪': food['脂肪'],
    '钙': food['钙'] + 8 * 0.4004 * 1000,      # 碳酸钙8g
    '磷': food['磷'],
    '铁': food['铁'],                             # ← 无铁补充
    '锌': food['锌'],                             # ← 无锌补充
    '铜': food['铜'],
    '锰': food['锰'] + 10,                       # 锰片1粒
    '钾': food['钾'],
    '钠': food['钠'] + 1.5 * 0.3934 * 1000,     # 碘盐1.5g
    '碘': iodine_current + iodine_deficit,        # 碘盐+碘化钾补足
    '硒': food['硒'],
    '牛磺酸': food['牛磺酸'] * 0.4 + 1500,      # 烹饪损60% + 补1.5g
    'VA': food['VA'],
    'VD': food['VD'],                             # ← 无VD3
    'VE': food['VE'] + 4 * 100 * 0.6711,        # 双鲸VE 4粒
    'VB1': food['VB1'] + hengjian_tabs * hengjian['VB1'],
    'VB2': food['VB2'] + hengjian_tabs * hengjian['VB2'],
    'VB3': food['VB3'] + hengjian_tabs * hengjian['VB3'],
    'VB6': food['VB6'] + hengjian_tabs * hengjian['VB6'],
    'VB12': food['VB12'] + hengjian_tabs * hengjian['VB12'],
    '花生四烯酸': food['花生四烯酸'],
    'EPA+DHA': food['EPA+DHA'],                   # ← 仅靠鲅鱼
    '亚油酸': food['亚油酸'],
    '氯化物': 1.5 * 0.6066 * 1000,
    '镁': food['镁'],
    '胆碱': food['胆碱'],
    '叶酸': food['叶酸'] + hengjian_tabs * hengjian['叶酸'],
    '泛酸': food['泛酸'] + hengjian_tabs * hengjian['VB5'],
}

print(f"\n总热量: {kcal:.1f} kcal (无鱼油)")
print(f"能量密度: {density:.3f} kcal/g")

# ============================================================
# NRC 2006 校验
# ============================================================
checks = [
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

print("\n" + "=" * 72)
print("NRC 2006 成猫 RA 校验 (per 1000 kcal)")
print("=" * 72)

header = f"{'营养素':<12} {'总量':>10} {'每1000kcal':>12} {'NRC最低':>10} {'NRC上限':>10} {'状态':>6}"
print(header)
print("-" * 72)

pass_count = 0
fail_count = 0
fail_items = []

for label, nrc_min, nrc_max, key, unit in checks:
    val = final[key]
    val_p1k = per1k(val)
    
    status = "✅"
    if val_p1k < nrc_min:
        status = "❌"
        fail_count += 1
        deficit_pct = (1 - val_p1k / nrc_min) * 100
        fail_items.append((label, val_p1k, nrc_min, unit, deficit_pct))
    elif nrc_max and val_p1k > nrc_max:
        status = "⚠️超"
        fail_count += 1
        fail_items.append((label, val_p1k, nrc_max, unit, -1))
    else:
        pass_count += 1
    
    nmax_str = f"{nrc_max}" if nrc_max else "—"
    print(f"{label:<12} {val:>10.1f}{unit:<4} {val_p1k:>10.1f} {nrc_min:>10} {nmax_str:>10} {status}")

# 钙磷比
ca_p = final['钙'] / final['磷']
cap_ok = 1.1 <= ca_p <= 1.5
print(f"\nCa:P = {ca_p:.3f} (要求1.1-1.5) {'✅' if cap_ok else '❌'}")

total_checks = pass_count + fail_count
print(f"\n{'='*72}")
print(f"结果: 通过 {pass_count}/{total_checks}  |  不达标 {fail_count}/{total_checks}")
print(f"{'='*72}")

if fail_items:
    print("\n❌ 不达标项详情 & 短期风险评估:")
    print("-" * 72)
    for label, actual, target, unit, deficit in fail_items:
        if deficit >= 0:
            risk = "⚠️ 低" if deficit < 30 else "⚠️ 中" if deficit < 60 else "🔴 高"
            if label in ['维生素D', '锌', '铁']:
                risk_note = "短期1周可接受(体内有储备)"
            elif label == 'EPA+DHA':
                risk_note = "鲅鱼已提供部分, 短期可接受"
            elif 'VB' in label or label == '维生素B1':
                risk_note = "水溶性维生素, 恒健VB部分补充"
            else:
                risk_note = "需关注"
            print(f"  {label}: {actual:.1f} vs 需要 {target} {unit}/1000kcal (缺{deficit:.0f}%) {risk} — {risk_note}")

# ============================================================
# 碘化钾补碘方案
# ============================================================
print(f"\n{'='*72}")
print("碘化钾补碘方案")
print(f"{'='*72}")
print(f"食材碘: {iodine_food:.1f} mcg")
print(f"碘盐碘: {iodine_salt:.1f} mcg")
print(f"当前碘 per 1000kcal: {per1k(iodine_current):.1f} mcg (需≥350)")
print(f"碘缺口: {iodine_deficit:.0f} mcg 元素碘")
print(f"需要碘化钾(KI): {ki_needed_mg:.2f} mg")
print(f"  → 如有碘化钾片10mg/片: 约 {ki_needed_mg/10:.2f} 片 (需精确称量)")
print(f"  → 如有碘化钾溶液(1%=10mg/ml): 约 {ki_needed_mg/10:.2f} ml")
print(f"  → 如有碘化钾溶液(10%=100mg/ml): 约 {ki_needed_mg/100:.3f} ml")

# ============================================================
# 每日分配
# ============================================================
print(f"\n{'='*72}")
print("每日分配方案")
print(f"{'='*72}")
daily_feed = 190  # g/day
print(f"成品 {finished:.0f}g ÷ 每日190g ≈ {finished/daily_feed:.1f} 天")

daily_a = 30 * 4.0 + 60 * density
daily_b = 30 * 4.0 + 50 * density
daily_c = 40 * 4.0 + 80 * density
print(f"\n| 猫 | 干粮 | 猫饭 | 总热量约 |")
print(f"|---|---:|---:|---:|")
print(f"| 公猫A | 30g | 60g | {daily_a:.0f} kcal |")
print(f"| 母猫B | 30g | 50g | {daily_b:.0f} kcal |")
print(f"| 幼猫C | 40g | 80g | {daily_c:.0f} kcal |")

# ============================================================
# 食材来源主要贡献分析
# ============================================================
print(f"\n{'='*72}")
print("关键缺失营养素 — 食材自供分析")
print(f"{'='*72}")

# 铁
iron_p1k = per1k(food['铁'])
print(f"\n铁: 食材提供 {food['铁']:.1f}mg = {iron_p1k:.1f} mg/1000kcal (NRC≥20)")
iron_contribs = [(names[i], amounts_7d[i]/100*nut['铁'][i]) for i in range(10) if amounts_7d[i]>0]
iron_contribs.sort(key=lambda x: -x[1])
for n, v in iron_contribs[:3]:
    print(f"  {n}: {v:.1f}mg")

# 锌
zinc_p1k = per1k(food['锌'])
print(f"\n锌: 食材提供 {food['锌']:.1f}mg = {zinc_p1k:.1f} mg/1000kcal (NRC≥18.5)")
zinc_contribs = [(names[i], amounts_7d[i]/100*nut['锌'][i]) for i in range(10) if amounts_7d[i]>0]
zinc_contribs.sort(key=lambda x: -x[1])
for n, v in zinc_contribs[:3]:
    print(f"  {n}: {v:.1f}mg")

# VD
vd_p1k = per1k(food['VD'])
print(f"\nVD: 食材提供 {food['VD']:.1f}IU = {vd_p1k:.1f} IU/1000kcal (NRC≥70)")
vd_contribs = [(names[i], amounts_7d[i]/100*nut['VD'][i]) for i in range(10) if amounts_7d[i]>0]
vd_contribs.sort(key=lambda x: -x[1])
for n, v in vd_contribs[:3]:
    print(f"  {n}: {v:.1f}IU")

# EPA+DHA
epadha_p1k = per1k(food['EPA+DHA'])
print(f"\nEPA+DHA: 鲅鱼提供 {food['EPA+DHA']:.1f}mg = {epadha_p1k:.1f} mg/1000kcal (NRC≥25)")

# VB12
vb12_total = final['VB12']
vb12_p1k = per1k(vb12_total)
print(f"\nVB12: 食材{food['VB12']:.1f}mcg + 恒健{hengjian_tabs*hengjian['VB12']:.1f}mcg = {vb12_total:.1f}mcg")
print(f"  = {vb12_p1k:.1f} mcg/1000kcal (NRC≥5.6)")

print(f"\n{'='*72}")
print("总结")
print(f"{'='*72}")
print(f"通过 {pass_count}/{total_checks} 项 NRC")
if fail_items:
    print(f"不达标 {fail_count} 项:")
    for label, actual, target, unit, deficit in fail_items:
        print(f"  - {label}: {actual:.1f}/{target} {unit}/1000kcal")
print()
print("关键判断:")
print("  1. VD 短期(1周)猫体内有脂溶性维生素储备, 不会立即缺乏")
print("  2. 铁/锌 肝脏和心脏提供了大部分, 差距看实际计算结果")
print("  3. EPA+DHA 鲅鱼59g自带, 看是否足够")
print("  4. 碘 必须用碘化钾补足, 不可省略")
print("  5. B族 恒健虽弱,但肝脏(B2/B3/B6/B12)贡献大,大部分B族应该够")
