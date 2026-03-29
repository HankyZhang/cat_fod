# -*- coding: utf-8 -*-
"""分析当前补充剂用量，找出哪些可以用小数精确化"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

spanish = {
    '能量': 139, '蛋白质': 19.29, '脂肪': 6.30,
    '磷': 171, '钙': 11, '铁': 0.44, '锌': 0.51, '铜': 0.046, '锰': 0.015,
    '钾': 446, '钠': 59, '碘': 35, '硒': 36.5,
    'VA': 98, 'VD': 292, 'VE': 0.42,
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
    'VA':          [50, 7, 31, 0, 520, 11078, 16898, spanish['VA'],   150, 80],
    'VD':          [0, 12, 0, 0, 82, 8, 49, spanish['VD'],   24, 4],
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
    '叶酸':        [6, 1, 72, 3, 47, 588, 290, spanish['叶酸'], 1, 25],
    '泛酸':        [1.01, 0.60, 2.51, 2.25, 1.53, 6.50, 7.17, spanish['泛酸'], 0.53, 1.60],
}

versions = {
    'A': [888, 600, 410, 445, 254, 127, 95, 127, 222, 0],
    'B': [288, 600, 410, 445, 254, 127, 95, 127, 222, 600],
    'C': [0, 600, 410, 445, 254, 127, 95, 127, 222, 900],
}

nrc_min = {
    '蛋白质': 50, '脂肪': 22.5, '钙': 720, '磷': 640, '钾': 1300,
    '钠': 170, '氯化物': 240, '镁': 100, '铁': 20, '锌': 18.5, '铜': 1.2,
    '锰': 1.2, '碘': 350, '硒': 75, '牛磺酸': 100, 'VA': 3333, 'VD': 70,
    'VE': 9.4, 'VB1': 1.4, 'VB2': 1.0, 'VB3': 10, 'VB6': 0.625, 'VB12': 5.6,
    '胆碱': 637, '叶酸': 188, '泛酸': 1.44, '花生四烯酸': 15, 'EPA+DHA': 25, '亚油酸': 1.4,
}

# 当前补充剂用量
current = {
    '碳酸钙粉': {'用量': '18g', '数值': 18},
    '鱼油': {'用量': '10粒', '数值': 10},
    'VD3': {'用量': '1粒', '数值': 1},
    'VE': {'用量': '8粒', '数值': 8},
    'B-50': {'用量': '2片', '数值': 2},
    '海带碘': {'用量': '7粒', '数值': 7},
    '牛磺酸': {'用量': '3g', '数值': 3},
    '锌片': {'用量': '1粒', '数值': 1},
    '螯合铁': {'用量': '1粒', '数值': 1},
    '锰片': {'用量': '1粒', '数值': 1},
}

print("=" * 70)
print("补充剂用量优化分析 —— 允许小数")
print("=" * 70)

results = {}

for vname, amounts in versions.items():
    def food_total(key):
        return sum(amounts[i] / 100 * nut[key][i] for i in range(10))
    food = {k: food_total(k) for k in nut}
    kcal = food['能量'] + 90  # +鱼油热量
    r = kcal / 1000

    # 碳酸钙: 需同时满足 NRC下限 和 Ca:P>=1.0
    min_ca_nrc = max(0, 720 * r - food['钙'])  # mg
    min_ca_ratio = max(0, food['磷'] * 1.0 - food['钙'])  # Ca:P>=1
    min_ca_mg = max(min_ca_nrc, min_ca_ratio)
    min_ca_g = min_ca_mg / 400.4
    results.setdefault('碳酸钙粉(g)', []).append(min_ca_g)

    # 铁
    min_fe = max(0, 20 * r - food['铁']) / 36
    results.setdefault('螯合铁(粒)', []).append(min_fe)

    # 锌
    min_zn = max(0, 18.5 * r - food['锌']) / 30
    results.setdefault('锌片(粒)', []).append(min_zn)

    # 锰
    min_mn = max(0, 1.2 * r - food['锰']) / 10
    results.setdefault('锰片(粒)', []).append(min_mn)

    # 碘 (牛磺酸胶囊含碘 3*25=75mcg)
    tau_iod = 75
    min_iod = max(0, 350 * r - food['碘'] - tau_iod) / 225
    results.setdefault('海带碘(粒)', []).append(min_iod)

    # VE (100IU/粒 = 67.11mg/粒)
    min_ve = max(0, 9.4 * r - food['VE']) / 67.11
    results.setdefault('VE(粒)', []).append(min_ve)

    # B-50 (各B族中最苛刻的决定片数)
    b50_items = []
    for bname, per_pill in [('VB1',50), ('VB2',50), ('VB3',50), ('VB6',50),
                              ('VB12',50), ('叶酸',400), ('泛酸',50)]:
        unit = 'mcg' if bname in ['VB12', '叶酸'] else 'mg'
        need = max(0, nrc_min[bname] * r - food[bname])
        pills = need / per_pill
        b50_items.append((bname, pills, need, food[bname], nrc_min[bname]*r, unit))
    limiting = max(b50_items, key=lambda x: x[1])
    results.setdefault('B-50(片)', []).append(limiting[1])
    results.setdefault('B-50限制', []).append(limiting[0])

    # 牛磺酸 (食物60%损失)
    tau_food = food['牛磺酸'] * 0.4
    min_tau = max(0, 100 * r - tau_food) / 1000
    results.setdefault('牛磺酸(g)', []).append(min_tau)

    # 鱼油 (纯NRC角度)
    min_fish = max(0, 25 * r - food['EPA+DHA']) / 300
    results.setdefault('鱼油(粒)', []).append(min_fish)

    # VD3
    vd_natural = food['VD'] / kcal * 1000
    results.setdefault('VD3_天然VD/1000kcal', []).append(vd_natural)

print(f"\n{'补充剂':<20} {'A最低':<10} {'B最低':<10} {'C最低':<10} {'三版取max':<10} {'当前用量':<10} {'结论'}")
print("-" * 90)

supp_order = ['碳酸钙粉(g)', '鱼油(粒)', 'VE(粒)', 'B-50(片)', '海带碘(粒)',
              '牛磺酸(g)', '锌片(粒)', '螯合铁(粒)', '锰片(粒)']
current_vals = {
    '碳酸钙粉(g)': 18, '鱼油(粒)': 10, 'VE(粒)': 8, 'B-50(片)': 2,
    '海带碘(粒)': 7, '牛磺酸(g)': 3, '锌片(粒)': 1, '螯合铁(粒)': 1, '锰片(粒)': 1,
}

changes = []
for name in supp_order:
    vals = results[name]
    maxv = max(vals)
    cur = current_vals[name]
    ratio = cur / maxv if maxv > 0 else float('inf')

    if name == 'B-50(片)':
        limit_str = f"(限制={results['B-50限制'][vals.index(max(vals))]})"
    else:
        limit_str = ""

    if ratio > 2.5:
        conclusion = f"⚠️ 当前是最低的 {ratio:.1f}倍，有很大下调空间"
        changes.append((name, maxv, cur))
    elif ratio > 1.5:
        conclusion = f"✅ 当前是最低的 {ratio:.1f}倍，有一定余量"
    else:
        conclusion = f"✅ 当前是最低的 {ratio:.1f}倍，基本合理"

    print(f"{name:<20} {vals[0]:<10.3f} {vals[1]:<10.3f} {vals[2]:<10.3f} {maxv:<10.3f} {cur:<10} {conclusion} {limit_str}")

print(f"\n{'VD3(1粒)':<20} ", end="")
for v in results['VD3_天然VD/1000kcal']:
    print(f"{v:<10.1f} ", end="")
print(f"{'—':<10} {'1粒':<10} 建议加（天然已达标≥70，加了更稳）")

print("\n" + "=" * 70)
print("可优化的补充剂（当前用量是最低需求的2.5倍以上）：")
print("=" * 70)
for name, minv, curv in changes:
    # 建议值：取最低需求的1.5倍（留余量），然后到0.5对齐
    suggested = minv * 1.5
    # 向上到最近0.1
    import math
    suggested_round = math.ceil(suggested * 10) / 10
    print(f"\n  {name}: 当前={curv} → NRC最低需={minv:.3f} → 建议用 {suggested_round:.1f} (1.5倍安全边际)")

    if name == '鱼油(粒)':
        print(f"    ⚠️ 但鱼油不纯为了NRC EPA+DHA指标，还有：")
        print(f"       - 抗炎（omega-3 抗炎是鱼油的主要意义）")
        print(f"       - 配合VE防氧化")
        print(f"       - 鲅鱼自身EPA+DHA已远超NRC，鱼油更多是保险和抗炎")
        print(f"    → 建议：鱼油保持不变（10粒），或根据实际减到5-8粒")

# 最后做一个新补充剂方案的完整29项验证
print("\n" + "=" * 70)
print("如果要精简，哪些补充剂真的可以减？")
print("=" * 70)

print("""
1. 碳酸钙粉 18g → 最低需约8g(Ca:P约束)
   但钙粉便宜、安全上限极高(30g/1000kcal)，保持18g毫无风险，Ca:P=1.2很健康。
   → 建议：保持18g不变。减了没好处，Ca:P会接近1.0红线。

2. 鱼油 10粒 → NRC角度 0粒就够（鲅鱼自带EPA+DHA远超NRC）
   但鱼油的omega-3抗炎作用不在NRC范围内。
   → 建议：保持10粒不变。

3. VE 8粒 → 最低需约0.6粒
   这是最明显可下调的！当前是NRC最低的13倍！
   → 可以调到 1-2粒。但注意VE配合鱼油防氧化的惯例比例。
   
4. B-50 2片 → 最低需约0.01片
   B族食物已经非常充足（肝脏含量极高），B-50主要是兜底保险。
   → 可以调到 0.5-1片。

5. 海带碘 7粒 → 最低需约4.8粒
   → 可以调到 5粒。

6. 牛磺酸 3g → 最低需约0.19g
   但牛磺酸有60%烹饪损失是最坏估计，且猫对牛磺酸需求高。
   → 建议：保持3g（牛磺酸便宜、安全上限极高、猫需求特殊）。

7. 锌 1粒 → 最低需约0.0粒（食物已够）
   → 可以调到 0.5粒。但锌也是安全的保险项。

8. 铁 1粒 → 最低需约0.0粒（食物已够，鸡心牛心鸡肝铁极丰富）
   → 可以调到 0.5粒。

9. 锰 1粒 → 最低需约0.4粒
   → 可以调到 0.5粒。
""")
