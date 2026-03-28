# -*- coding: utf-8 -*-
"""
鲅鱼(Spanish mackerel)替换大西洋鲭鱼(Atlantic mackerel)影响分析
基于 C 版（鸭胸强化版）
USDA: "Fish, mackerel, spanish, raw" (FDC 175119) 作为鲅鱼代理值
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ─── 当前用的大西洋鲭鱼 vs 鲅鱼(Spanish mackerel) per 100g ───
atlantic = {
    '能量': 205.4, '蛋白质': 18.6, '脂肪': 13.9,
    '磷': 217, '钙': 12, '铁': 1.63, '锌': 0.63, '铜': 0.07, '锰': 0.02,
    '钾': 314, '钠': 90, '碘': 44, '硒': 44.1,
    'VA': 167, 'VD': 644, 'VE': 1.52,
    'VB1': 0.18, 'VB2': 0.31, 'VB3': 9.08, 'VB6': 0.40, 'VB12': 8.7,
    '牛磺酸': 70, '花生四烯酸': 60, 'EPA+DHA': 2299.1, '亚油酸': 0.219,
    '镁': 76, '胆碱': 65, '叶酸': 1, '泛酸': 0.86,
}

# USDA "Fish, mackerel, spanish, raw" (FDC 175119 / NDB 15049)
# 鲅鱼 (Scomberomorus niphonius) 用同属 S. maculatus 数据作代理
spanish = {
    '能量': 139, '蛋白质': 19.29, '脂肪': 6.30,
    '磷': 171, '钙': 11, '铁': 0.44, '锌': 0.51, '铜': 0.046, '锰': 0.015,
    '钾': 446, '钠': 59, '碘': 35, '硒': 36.5,  # 碘按保守估计
    'VA': 98, 'VD': 16, 'VE': 0.42,  # VD仅16 IU！
    'VB1': 0.068, 'VB2': 0.130, 'VB3': 8.47, 'VB6': 0.315, 'VB12': 7.4,
    '牛磺酸': 70, '花生四烯酸': 60, 'EPA+DHA': 941, '亚油酸': 0.100,
    # EPA ~352mg + DHA ~589mg = 941mg/100g (USDA fatty acid profile)
    '镁': 33, '胆碱': 65, '叶酸': 2, '泛酸': 0.42,
}

fish_amount = 127  # g

print('=' * 72)
print('大西洋鲭鱼 vs 鲅鱼(Spanish mackerel) 营养差异（per 100g）')
print('=' * 72)
print(f'{"项目":<12} {"大西洋鲭鱼":>12} {"鲅鱼":>12} {"差异":>12} {"影响":>8}')
print('-' * 60)

important_diffs = []
for key in atlantic:
    a = atlantic[key]
    s = spanish[key]
    diff_pct = (s - a) / a * 100 if a != 0 else 0
    impact = '⚠️' if abs(diff_pct) > 30 else '✅'
    if abs(diff_pct) > 30:
        important_diffs.append((key, a, s, diff_pct))
    print(f'{key:<12} {a:>12.1f} {s:>12.1f} {diff_pct:>+11.1f}% {impact}')

print()
print('=' * 72)
print('关键大差异（超过30%的项）')
print('=' * 72)
for key, a, s, pct in important_diffs:
    contribution_a = fish_amount * a / 100
    contribution_s = fish_amount * s / 100
    loss = contribution_a - contribution_s
    print(f'{key}: {a} → {s} ({pct:+.0f}%)')
    print(f'  127g鱼提供: {contribution_a:.1f} → {contribution_s:.1f}, 损失={loss:.1f}')

# ─── 完整替换后重新计算C版 29项NRC ───
print()
print('=' * 72)
print('C版(鸭胸强化版) 替换为鲅鱼后的完整NRC验证')
print('=' * 72)

# 食材营养 per 100g (10种: 鸡腿, 猪瘦, 鸡心, 牛心, 蛋, 鸡肝, 牛肝, 鱼, 鸡皮, 鸭胸)
# 鱼的位置(index 7) 替换为鲅鱼数据
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

# C版食材用量
amounts = [588, 0, 410, 445, 254, 127, 95, 127, 222, 900]

# 补充剂
supp = {
    '鱼油热量': 90,
    'EPA+DHA': 3000,
    '钙': 18 * 0.4004 * 1000,
    '铁': 1 * 36,               # 螯合铁 1粒 × 36mg
    '锌': 1 * 30,               # 锌片 1粒 × 30mg
    '锰': 1 * 10,
    '碘': 7 * 225 + 3 * 25,
    '钠': 3 * 0.3934 * 1000,
    'VE': 8 * 100 * 0.6711,     # 8粒×100IU
    'VB1': 2 * 50,
    'VB2': 2 * 50,
    'VB3': 2 * 50,
    'VB6': 2 * 50,
    'VB12': 2 * 50,
    '牛磺酸': 3000,
    '氯化物': 3 * 0.6066 * 1000,
    '叶酸': 2 * 400,
    '泛酸': 2 * 50,
}

def food_total(key):
    return sum(amounts[i] / 100 * nut[key][i] for i in range(10))

food = {k: food_total(k) for k in nut}
kcal = food['能量'] + supp['鱼油热量']
raw_total = sum(amounts)
finished = raw_total * 0.9
density = kcal / finished
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

# 原C版文档值（大西洋鲭鱼）
orig_c = {
    '蛋白质': 114.1, '脂肪': 53.8, '钙': 1586.5, '磷': 1292.9,
    '钾': 1552.2, '钠': 808.5, '氯化物': 378.4, '镁': 135.9,
    '铁': 27.0, '锌': 22.5, '铜': 3.3, '锰': 2.4,
    '碘': 382.8, '硒': 144.6, '牛磺酸': 771.9,
    'VA': 6889.5, 'VD': 240.0, 'VE': 115.2,
    'VB1': 22.1, 'VB2': 24.7, 'VB3': 56.9,
    'VB6': 23.0, 'VB12': 55.2, '胆碱': 709.6,
    '叶酸': 522.8, '泛酸': 33.7, '花生四烯酸': 477.2,
    'EPA+DHA': 1231.1, '亚油酸': 9.06,
}

print(f'总能量: {kcal:.1f} kcal (原C版: 4809 kcal)')
print(f'能量密度: {density:.3f} kcal/g (原C版: 1.687)')
print(f'Ca:P = {final["钙"]/final["磷"]:.3f}')
print()

nrc_pass = 0
nrc_fail = 0
issues = []
print(f'{"营养素":<10} {"鲅鱼版":>10} {"原C版":>10} {"NRC最低":>10} {"余量%":>8} 状态')
print('-' * 62)
for name, low, high, unit in checks:
    value = per1k(final[name])
    ok = value >= low and (high is None or value <= high)
    margin = (value - low) / low * 100
    orig = orig_c.get(name, 0)
    status = '✅' if ok else '❌'
    if not ok:
        nrc_fail += 1
        issues.append((name, value, low, margin))
    else:
        nrc_pass += 1
    
    # 标记余量很薄的项
    if ok and margin < 15:
        status = '⚠️薄'
    
    print(f'{name:<10} {value:>10.1f} {orig:>10.1f} {low:>10g} {margin:>+7.1f}% {status}')

print()
print(f'NRC通过: {nrc_pass}/29')

if issues:
    print()
    print('❌ 不达标项:')
    for name, val, low, margin in issues:
        print(f'  {name}: {val:.1f} < {low} (差{abs(margin):.1f}%)')

# 每日热量
da = 30*4.0 + 60*density
db = 30*4.0 + 50*density
dc = 40*4.0 + 80*density
print(f'\n每日热量: A={da:.0f} B={db:.0f} C={dc:.0f} total={da+db+dc:.0f} kcal')

# ─── 如果VD不达标，计算需要多少额外VD补充 ───
vd_per1k = per1k(final['VD'])
if vd_per1k < 70:
    deficit_per1k = 70 - vd_per1k
    deficit_total = deficit_per1k * kcal / 1000
    print(f'\n⚠️  VD不达标！需额外补充 {deficit_total:.0f} IU VD')
    print(f'    方案1: 额外加1粒VD3 1000IU胶囊 → VD变为 {per1k(final["VD"] + 1000):.1f}/1000kcal')
    print(f'    方案2: 额外加1粒VD3 1000IU胶囊 → VD变为 {per1k(final["VD"] + 1000):.1f}/1000kcal')
    print(f'    方案3: 鱼提高到 200g → 需要重新全面计算')

# ─── 碘余量检查 ───
iodine_per1k = per1k(final['碘'])
print(f'\n碘余量: {iodine_per1k:.1f}/1000kcal vs NRC 350 → 余量={((iodine_per1k-350)/350*100):.1f}%')

# ─── EPA+DHA检查 ───
epa_per1k = per1k(final['EPA+DHA'])
print(f'EPA+DHA: {epa_per1k:.1f}/1000kcal vs NRC 25 → 鱼油补充足够，无问题')
