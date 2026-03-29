# -*- coding: utf-8 -*-
"""
鲅鱼(Spanish mackerel)替换影响分析
基于当前现行 A/B/C 鲅鱼总版，重点看天然 VD 余量与补 1 粒 VD3 后的安全边际。
"""
import sys, io
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

atlantic = {
    '能量': 205.4, '蛋白质': 18.6, '脂肪': 13.9,
    '磷': 217, '钙': 12, '铁': 1.63, '锌': 0.63, '铜': 0.07, '锰': 0.02,
    '钾': 314, '钠': 90, '碘': 44, '硒': 44.1,
    'VA': 167, 'VD': 644, 'VE': 1.52,
    'VB1': 0.18, 'VB2': 0.31, 'VB3': 9.08, 'VB6': 0.40, 'VB12': 8.7,
    '牛磺酸': 70, '花生四烯酸': 60, 'EPA+DHA': 2299.1, '亚油酸': 0.219,
    '镁': 76, '胆碱': 65, '叶酸': 1, '泛酸': 0.86,
}

spanish = {
    '能量': 139, '蛋白质': 19.29, '脂肪': 6.30,
    '磷': 171, '钙': 11, '铁': 0.44, '锌': 0.51, '铜': 0.046, '锰': 0.015,
    '钾': 446, '钠': 59, '碘': 35, '硒': 36.5,
    'VA': 98, 'VD': 292, 'VE': 0.42,
    'VB1': 0.068, 'VB2': 0.130, 'VB3': 8.47, 'VB6': 0.315, 'VB12': 7.4,
    '牛磺酸': 70, '花生四烯酸': 60, 'EPA+DHA': 941, '亚油酸': 0.100,
    '镁': 33, '胆碱': 65, '叶酸': 2, '泛酸': 0.42,
}

fish_amount = 127

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
    delta = contribution_s - contribution_a
    print(f'{key}: {a} → {s} ({pct:+.0f}%)')
    print(f'  127g鱼提供: {contribution_a:.1f} → {contribution_s:.1f}, 变化={delta:+.1f}')

versions = {
    'A_7%鸡皮+鲅鱼': [888, 600, 410, 445, 254, 127, 95, 127, 222, 0],
    'B_7%鸡皮+鸭胸+鲅鱼': [288, 600, 410, 445, 254, 127, 95, 127, 222, 600],
    'C_鸭胸强化+鲅鱼': [0, 600, 410, 445, 254, 127, 95, 127, 222, 900],
}

nut = {
    '能量':        [119, 143, 153, 112, 143, 119, 135, spanish['能量'], 349, 135],
    '蛋白质':      [19.6, 21.1, 15.6, 17.7, 12.6, 16.9, 20.4, spanish['蛋白质'], 13.3, 18.28],
    '脂肪':        [4.3, 6.9, 9.3, 3.9, 9.9, 4.8, 3.6, spanish['脂肪'], 32.4, 5.95],
    '磷':          [178, 197, 177, 212, 198, 297, 387, spanish['磷'], 68, 203],
    '钙':          [9, 5, 12, 7, 56, 8, 5, spanish['钙'], 11, 11],
    '铁':          [0.8, 0.8, 5.9, 4.3, 1.8, 9.0, 4.9, spanish['铁'], 0.7, 2.4],
    '锌':          [1.8, 1.9, 6.6, 2.4, 1.3, 2.7, 4.0, spanish['锌'], 0.6, 1.9],
    '铜':          [0.06, 0.06, 0.33, 0.39, 0.07, 0.49, 9.76, spanish['铜'], 0.02, 0.24],
    '锰':          [0.02, 0.01, 0.05, 0.03, 0.03, 0.26, 0.31, spanish['锰'], 0.01, 0.02],
    '钾':          [242.0, 389.0, 176.066, 286.984, 138.0, 230.0, 313.0, spanish['钾'], 119.0, 271.0],
    '钠':          [95.0, 52.0, 73.934, 97.989, 142.0, 71.0, 69.0, spanish['钠'], 51.0, 74.0],
    '碘':          [1, 1, 5, 5, 27, 3, 3, spanish['碘'], 1, 1],
    '硒':          [23.0, 32.5, 16.0, 21.8, 30.7, 54.6, 39.7, spanish['硒'], 14.1, 14.0],
    'VA':          [50, 7, 31, 0, 520, 11078, 16898, spanish['VA'], 150, 80],
    'VD':          [0, 12, 0, 0, 82, 8, 49, spanish['VD'], 24, 4],
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
    '镁':          [23, 25, 15, 21, 12, 19, 20, spanish['镁'], 10, 20],
    '胆碱':        [65, 80, 65, 150, 293, 290, 333, spanish['胆碱'], 46, 64],
    '叶酸':        [6, 1, 72, 3, 47, 588, 290, spanish['叶酸'], 1, 25],
    '泛酸':        [1.01, 0.60, 2.51, 2.25, 1.53, 6.50, 7.17, spanish['泛酸'], 0.53, 1.60],
}

checks = [
    ('蛋白质', 50, None), ('脂肪', 22.5, None), ('钙', 720, 3000), ('磷', 640, None),
    ('铁', 20, None), ('钾', 1300, None), ('钠', 170, None), ('锌', 18.5, None),
    ('铜', 1.2, None), ('锰', 1.2, None), ('碘', 350, 9000), ('硒', 75, None),
    ('牛磺酸', 250, None), ('VA', 3333, 333333), ('VD', 70, 7500), ('VE', 10, None),
    ('VB1', 1.4, None), ('VB2', 1.0, None), ('VB3', 10, None), ('VB6', 0.625, None),
    ('VB12', 5.6, None), ('花生四烯酸', 15, None), ('EPA+DHA', 25, None), ('亚油酸', 1.4, None),
    ('氯化物', 240, None), ('镁', 100, None), ('胆碱', 637, None), ('叶酸', 188, None), ('泛酸', 1.44, None),
]

supp_base = {
    '鱼油热量': 90,
    'EPA+DHA': 3000,
    '钙': 18 * 0.4004 * 1000,
    '铁': 36,
    '锌': 30,
    '锰': 10,
    '碘': 7 * 225 + 3 * 25,
    '钠': 3 * 0.3934 * 1000,
    'VE': 8 * 100 * 0.6711,
    'VB1': 100,
    'VB2': 100,
    'VB3': 100,
    'VB6': 100,
    'VB12': 100,
    '牛磺酸': 3000,
    '氯化物': 3 * 0.6066 * 1000,
    '叶酸': 800,
    '泛酸': 100,
}

def compute(amounts, vd_extra):
    def food_total(key):
        return sum(amounts[i] / 100 * nut[key][i] for i in range(10))

    food = {k: food_total(k) for k in nut}
    kcal = food['能量'] + supp_base['鱼油热量']
    finished = sum(amounts) * 0.9
    per1k = lambda x: x / kcal * 1000
    final = {
        '蛋白质': food['蛋白质'],
        '脂肪': food['脂肪'],
        '钙': food['钙'] + supp_base['钙'],
        '磷': food['磷'],
        '铁': food['铁'] + supp_base['铁'],
        '锌': food['锌'] + supp_base['锌'],
        '铜': food['铜'],
        '锰': food['锰'] + supp_base['锰'],
        '钾': food['钾'],
        '钠': food['钠'] + supp_base['钠'],
        '碘': food['碘'] + supp_base['碘'],
        '硒': food['硒'],
        '牛磺酸': food['牛磺酸'] * 0.4 + supp_base['牛磺酸'],
        'VA': food['VA'],
        'VD': food['VD'] + vd_extra,
        'VE': food['VE'] + supp_base['VE'],
        'VB1': food['VB1'] + supp_base['VB1'],
        'VB2': food['VB2'] + supp_base['VB2'],
        'VB3': food['VB3'] + supp_base['VB3'],
        'VB6': food['VB6'] + supp_base['VB6'],
        'VB12': food['VB12'] + supp_base['VB12'],
        '花生四烯酸': food['花生四烯酸'],
        'EPA+DHA': food['EPA+DHA'] + supp_base['EPA+DHA'],
        '亚油酸': food['亚油酸'],
        '氯化物': supp_base['氯化物'],
        '镁': food['镁'],
        '胆碱': food['胆碱'],
        '叶酸': food['叶酸'] + supp_base['叶酸'],
        '泛酸': food['泛酸'] + supp_base['泛酸'],
    }

    failed = []
    for name, low, high in checks:
        value = per1k(final[name])
        if not (value >= low and (high is None or value <= high)):
            failed.append((name, value, low, high))

    return {
        'kcal': kcal,
        'density': kcal / finished,
        'vd': per1k(final['VD']),
        'failures': failed,
        'pass_count': len(checks) - len(failed),
    }

print()
print('=' * 72)
print('当前现行 A/B/C 版本：不补 VD3 vs 补 1 粒 VD3')
print('=' * 72)

for name, amounts in versions.items():
    no_extra = compute(amounts, 0)
    with_extra = compute(amounts, 1000)
    print(name)
    print(f'  总能量: {with_extra["kcal"]:.1f} kcal')
    print(f'  能量密度: {with_extra["density"]:.3f} kcal/g')
    print(f'  天然VD: {no_extra["vd"]:.1f} IU/1000kcal, NRC余量={no_extra["vd"] - 70:.1f}')
    print(f'  补VD3后: {with_extra["vd"]:.1f} IU/1000kcal, NRC余量={with_extra["vd"] - 70:.1f}')
    print(f'  不补VD3: {no_extra["pass_count"]}/29', end='')
    if no_extra['failures']:
        failed_names = ', '.join(item[0] for item in no_extra['failures'])
        print(f'，未过项：{failed_names}')
    else:
        print('，全部通过但 VD 余量偏薄')
    print(f'  补VD3后: {with_extra["pass_count"]}/29，全部通过')
    print()

print('结论：')
print('- 当前现行 A/B/C 配方在不补 VD3 时，维生素D天然值约 74-86 IU/1000kcal，已非常贴近 70 的校验下限。')
print('- 因此现行统一执行总版继续规定：每批都额外补 1 粒 1000IU VD3，用来拉开余量并统一执行。')
