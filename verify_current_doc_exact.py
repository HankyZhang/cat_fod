# -*- coding: utf-8 -*-
import sys, io
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('=' * 72)
print('当前执行文档 · C版（鸭胸强化 + 鲅鱼）精确配方复核')
print('=' * 72)

spanish = {
    '能量': 139, '蛋白质': 19.29, '脂肪': 6.30,
    '磷': 171, '钙': 11, '铁': 0.44, '锌': 0.51, '铜': 0.046, '锰': 0.015,
    '钾': 446, '钠': 59, '碘': 35, '硒': 36.5,
    'VA': 98, 'VD': 292, 'VE': 0.42,
    'VB1': 0.068, 'VB2': 0.130, 'VB3': 8.47, 'VB6': 0.315, 'VB12': 7.4,
    '牛磺酸': 70, '花生四烯酸': 60, 'EPA+DHA': 941, '亚油酸': 0.100,
    '镁': 33, '胆碱': 65, '叶酸': 2, '泛酸': 0.42,
}

amounts = {
    '鸡腿肉': 0,
    '猪瘦肉': 600,
    '鸡心': 410,
    '牛心': 445,
    '鸡蛋': 254,
    '鸡肝': 127,
    '牛肝': 95,
    '鲅鱼': 127,
    '鸡皮': 222,
    '鸭胸肉': 900,
}

nutrients = {
    '能量': [119, 143, 153, 112, 143, 119, 135, spanish['能量'], 349, 135],
    '蛋白质': [19.6, 21.1, 15.6, 17.7, 12.6, 16.9, 20.4, spanish['蛋白质'], 13.3, 18.28],
    '脂肪': [4.3, 6.9, 9.3, 3.9, 9.9, 4.8, 3.6, spanish['脂肪'], 32.4, 5.95],
    '磷': [178, 197, 177, 212, 198, 297, 387, spanish['磷'], 68, 203],
    '钙': [9, 5, 12, 7, 56, 8, 5, spanish['钙'], 11, 11],
    '铁': [0.8, 0.8, 5.9, 4.3, 1.8, 9.0, 4.9, spanish['铁'], 0.7, 2.4],
    '锌': [1.8, 1.9, 6.6, 2.4, 1.3, 2.7, 4.0, spanish['锌'], 0.6, 1.9],
    '铜': [0.06, 0.06, 0.33, 0.39, 0.07, 0.49, 9.76, spanish['铜'], 0.02, 0.24],
    '锰': [0.02, 0.01, 0.05, 0.03, 0.03, 0.26, 0.31, spanish['锰'], 0.01, 0.02],
    '钾': [242.0, 389.0, 176.066, 286.984, 138.0, 230.0, 313.0, spanish['钾'], 119.0, 271.0],
    '钠': [95.0, 52.0, 73.934, 97.989, 142.0, 71.0, 69.0, spanish['钠'], 51.0, 74.0],
    '碘': [1, 1, 5, 5, 27, 3, 3, spanish['碘'], 1, 1],
    '硒': [23.0, 32.5, 16.0, 21.8, 30.7, 54.6, 39.7, spanish['硒'], 14.1, 14.0],
    'VA': [50, 7, 31, 0, 520, 11078, 16898, spanish['VA'], 150, 80],
    'VD': [0, 12, 0, 0, 82, 8, 49, spanish['VD'], 24, 4],
    'VE': [0.2, 0.5, 0.7, 0.2, 1.1, 0.7, 0.5, spanish['VE'], 0.3, 0.7],
    'VB1': [0.07, 0.81, 0.13, 0.24, 0.04, 0.31, 0.19, spanish['VB1'], 0.01, 0.36],
    'VB2': [0.16, 0.23, 0.73, 0.91, 0.46, 1.78, 2.76, spanish['VB2'], 0.07, 0.47],
    'VB3': [5.3, 5.0, 4.8, 7.4, 0.1, 9.7, 13.2, spanish['VB3'], 2.5, 5.3],
    'VB6': [0.33, 0.42, 0.29, 0.28, 0.14, 0.85, 1.08, spanish['VB6'], 0.05, 0.34],
    'VB12': [0.4, 0.6, 7.3, 8.6, 0.9, 16.6, 59.3, spanish['VB12'], 0.3, 0.4],
    '牛磺酸': [40, 50, 145, 160, 20, 30, 40, spanish['牛磺酸'], 10, 0],
    '花生四烯酸': [50, 70, 84, 25, 155, 260, 200, spanish['花生四烯酸'], 250, 0],
    'EPA+DHA': [0, 0, 0, 0, 0, 0, 0, spanish['EPA+DHA'], 0, 0],
    '亚油酸': [0.748, 0.49, 1.918, 0.395, 1.554, 0.475, 0.299, spanish['亚油酸'], 8.288, 0.752],
    '镁': [23, 25, 15, 21, 12, 19, 20, spanish['镁'], 10, 20],
    '胆碱': [65, 80, 65, 150, 293, 290, 333, spanish['胆碱'], 46, 64],
    '叶酸': [6, 1, 72, 3, 47, 588, 290, spanish['叶酸'], 1, 25],
    '泛酸': [1.01, 0.60, 2.51, 2.25, 1.53, 6.50, 7.17, spanish['泛酸'], 0.53, 1.60],
}

vals = list(amounts.values())
raw_total = sum(vals)
finished = raw_total * 0.9

def total(arr):
    return sum(v / 100 * a for v, a in zip(vals, arr))

food = {name: total(arr) for name, arr in nutrients.items()}

supp = {
    '鱼油热量': 90,
    'EPA+DHA': 3000,
    '钙': 18 * 0.4004 * 1000,
    '铁': 0.5 * 36,              # 螯合铁 0.5粒
    '锌': 0.5 * 30,              # 锌片 0.5粒
    '锰': 0.5 * 10,              # 锰片 0.5粒
    '碘': 7 * 225 + 3 * 25,
    '钠': 3 * 0.3934 * 1000,
    'VE': 2 * 100 * 0.6711,     # VE 2粒
    'VD_extra': 1000,
    'VB1': 0.5 * 50,            # B-50 0.5片
    'VB2': 0.5 * 50,
    'VB3': 0.5 * 50,
    'VB6': 0.5 * 50,
    'VB12': 0.5 * 50,
    '牛磺酸': 3000,
    '氯化物': 3 * 0.6066 * 1000,
    '叶酸': 0.5 * 400,
    '泛酸': 0.5 * 50,
}

kcal = food['能量'] + supp['鱼油热量']
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
    'VD': food['VD'] + supp['VD_extra'],
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

expected = {
    'raw_total': 3180,
    'finished': 2862.0,
    'kcal': 4882.6,
    'density': 1.706,
    'ca_p': 1.209,
}

print(f'原料总量: {raw_total} g')
print(f'成品重量(90%出成率): {finished:.1f} g')
print(f'总能量(含鱼油+VD3): {kcal:.1f} kcal')
print(f'能量密度: {kcal / finished:.3f} kcal/g')
print()

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

issues = []
print(f"{'营养素':<10} {'每1000kcal':>12} {'NRC最低':>10} {'NRC上限':>10}  状态")
print('-' * 62)
for name, low, high, unit in checks:
    value = per1k(final[name])
    ok = value >= low and (high is None or value <= high)
    if not ok:
        issues.append((name, value, low, high))
    high_text = '—' if high is None else f'{high:g}'
    print(f"{name:<10} {value:>12.1f} {low:>10g} {high_text:>10}  {'✅' if ok else '❌'}")

print()
print(f"Ca:P = {final['钙']:.1f}/{final['磷']:.1f} = {final['钙'] / final['磷']:.3f}")
print(f"牛磺酸/kg成品 = {final['牛磺酸'] / (finished / 1000):.1f} mg/kg")
print(f"维生素D总量 = {final['VD']:.1f} IU -> {per1k(final['VD']):.1f}/1000kcal")
print(f"EPA+DHA总量 = {final['EPA+DHA']:.1f} mg -> {per1k(final['EPA+DHA']):.1f}/1000kcal")

catfood_kcal_per_g = kcal / finished
cat_a = 30 * 4.0 + 60 * catfood_kcal_per_g
cat_b = 30 * 4.0 + 50 * catfood_kcal_per_g
cat_c = 40 * 4.0 + 80 * catfood_kcal_per_g
print(f"分猫能量: A={cat_a:.1f}, B={cat_b:.1f}, C={cat_c:.1f}, 合计={cat_a + cat_b + cat_c:.1f} kcal/天")

meta_issues = []
if raw_total != expected['raw_total']:
    meta_issues.append(f"原料总量={raw_total}，预期={expected['raw_total']}")
if abs(finished - expected['finished']) > 0.5:
    meta_issues.append(f"成品重量={finished:.1f}，预期={expected['finished']:.1f}")
if abs(kcal - expected['kcal']) > 0.2:
    meta_issues.append(f"总能量={kcal:.1f}，预期={expected['kcal']:.1f}")
if abs(kcal / finished - expected['density']) > 0.002:
    meta_issues.append(f"能量密度={kcal / finished:.3f}，预期={expected['density']:.3f}")
if abs(final['钙'] / final['磷'] - expected['ca_p']) > 0.002:
    meta_issues.append(f"Ca:P={final['钙'] / final['磷']:.3f}，预期={expected['ca_p']:.3f}")

print()
if issues or meta_issues:
    print(f'存在 {len(issues)} 项 NRC 问题，{len(meta_issues)} 项元数据偏差')
    for row in issues:
        print(row)
    for row in meta_issues:
        print(row)
else:
    print('当前 C 版配方与现行执行文档一致，29/29 核心营养指标达标')
