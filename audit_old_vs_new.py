# -*- coding: utf-8 -*-
"""
审计脚本：对比旧版 (VE=8, B-50=2, 锌=1, 铁=1, 锰=1) 
         vs 新版 (VE=2, B-50=0.5, 锌=0.5, 铁=0.5, 锰=0.5)
逐项拆解食物贡献、补充剂贡献、NRC 阈值、实际/阈值比
"""
import sys, io
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── 食材营养 (per 100g raw) ──
# 顺序: 鸡腿, 猪瘦, 鸡心, 牛心, 蛋, 鸡肝, 牛肝, 鲅鱼, 鸡皮, 鸭胸
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

versions = {
    'A': [888, 600, 410, 445, 254, 127, 95, 127, 222, 0],
    'B': [288, 600, 410, 445, 254, 127, 95, 127, 222, 600],
    'C': [0,   600, 410, 445, 254, 127, 95, 127, 222, 900],
}

# ── NRC 2006 RA (per 1000 kcal) ──
nrc = {
    '蛋白质': (50, None, 'g'),
    '脂肪': (22.5, None, 'g'),
    '钙': (720, 3000, 'mg'),
    '磷': (640, None, 'mg'),
    '铁': (20, None, 'mg'),
    '钾': (1300, None, 'mg'),
    '钠': (170, None, 'mg'),
    '锌': (18.5, None, 'mg'),
    '铜': (1.2, None, 'mg'),
    '锰': (1.2, None, 'mg'),
    '碘': (350, 9000, 'mcg'),
    '硒': (75, None, 'mcg'),
    '牛磺酸': (250, None, 'mg'),
    'VA': (3333, 333333, 'IU'),
    'VD': (70, 7500, 'IU'),
    'VE': (10, None, 'mg'),
    'VB1': (1.4, None, 'mg'),
    'VB2': (1.0, None, 'mg'),
    'VB3': (10, None, 'mg'),
    'VB6': (0.625, None, 'mg'),
    'VB12': (5.6, None, 'mcg'),
    '花生四烯酸': (15, None, 'mg'),
    'EPA+DHA': (25, None, 'mg'),
    '亚油酸': (1.4, None, 'g'),
    '氯化物': (240, None, 'mg'),
    '镁': (100, None, 'mg'),
    '胆碱': (637, None, 'mg'),
    '叶酸': (188, None, 'mcg'),
    '泛酸': (1.44, None, 'mg'),
}

# ── 两套补充剂方案 ──
def make_supp(ve_pills, b50_pills, zn_pills, fe_pills, mn_pills):
    return {
        '鱼油热量': 90,
        'EPA+DHA': 3000,
        '钙': 18 * 0.4004 * 1000,
        '铁': fe_pills * 36,
        '锌': zn_pills * 30,
        '锰': mn_pills * 10,
        '碘': 7 * 225 + 3 * 25,
        '钠': 3 * 0.3934 * 1000,
        'VE': ve_pills * 100 * 0.6711,
        'VD_extra': 1000,
        'VB1': b50_pills * 50,
        'VB2': b50_pills * 50,
        'VB3': b50_pills * 50,
        'VB6': b50_pills * 50,
        'VB12': b50_pills * 50,
        '牛磺酸': 3000,
        '氯化物': 3 * 0.6066 * 1000,
        '叶酸': b50_pills * 400,
        '泛酸': b50_pills * 50,
    }

OLD = make_supp(ve_pills=8, b50_pills=2, zn_pills=1, fe_pills=1, mn_pills=1)
NEW = make_supp(ve_pills=2, b50_pills=0.5, zn_pills=0.5, fe_pills=0.5, mn_pills=0.5)

def calc_version(amounts, supp):
    def food_total(key):
        return sum(amounts[i] / 100 * nut[key][i] for i in range(10))
    food = {k: food_total(k) for k in nut}
    kcal = food['能量'] + supp['鱼油热量']
    
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
    return food, final, kcal

# ═══════════════════════════════════════════════════════
# 第一部分：纯食物对 NRC 的覆盖率（不含任何补充剂）
# ═══════════════════════════════════════════════════════
print("=" * 80)
print("第一部分：纯食物(+鱼油热量)对 NRC 的覆盖率 —— 看食物到底缺多少")
print("=" * 80)

# 只关心变更的5项
focus_items = ['VE', 'VB1', 'VB2', 'VB3', 'VB6', 'VB12', '叶酸', '泛酸', '锌', '铁', '锰']

for vname in ['A', 'B', 'C']:
    amounts = versions[vname]
    food, _, kcal_base = calc_version(amounts, make_supp(0, 0, 0, 0, 0))
    # kcal_base uses fish oil calories but zero supp nutrients
    kcal = sum(amounts[i] / 100 * nut['能量'][i] for i in range(10)) + 90
    r = kcal / 1000
    print(f"\n─── {vname}版 (总热量 {kcal:.0f} kcal, r={r:.3f}) ───")
    print(f"  {'指标':<10} {'食物总量':>10} {'NRC需求':>10} {'食物/NRC':>10} {'缺口':>10}")
    
    for item in focus_items:
        low, high, unit = nrc[item]
        need = low * r
        
        if item == '牛磺酸':
            food_val = food[item] * 0.4  # 60% cooking loss
        else:
            food_val = food[item]
        
        ratio = food_val / need if need > 0 else float('inf')
        gap = need - food_val
        gap_str = f"{gap:+.2f}" if gap > 0 else "充足"
        
        print(f"  {item:<10} {food_val:>10.2f} {need:>10.2f} {ratio:>9.1%} {gap_str:>10}")

# ═══════════════════════════════════════════════════════
# 第二部分：旧版 vs 新版 —— 29项逐项对比
# ═══════════════════════════════════════════════════════
print("\n\n" + "=" * 80)
print("第二部分：旧版(8/2/1/1/1) vs 新版(2/0.5/0.5/0.5/0.5) 逐项校验")
print("=" * 80)

# 只关注变更的指标做详细对比
changed_items = ['VE', 'VB1', 'VB2', 'VB3', 'VB6', 'VB12', '叶酸', '泛酸', '锌', '铁', '锰']

for vname in ['A', 'B', 'C']:
    amounts = versions[vname]
    food_old, final_old, kcal_old = calc_version(amounts, OLD)
    food_new, final_new, kcal_new = calc_version(amounts, NEW)
    
    # kcal should be same (same fish oil)
    kcal = kcal_old
    per1k = lambda x: x / kcal * 1000
    
    print(f"\n{'─'*80}")
    print(f"  {vname}版  (kcal={kcal:.0f})")
    print(f"  {'指标':<8} {'NRC下限':>10} {'旧版/1000k':>12} {'旧倍率':>8} {'新版/1000k':>12} {'新倍率':>8} {'新版?':>6}")
    print(f"  {'─'*70}")
    
    old_pass = 0
    new_pass = 0
    for item in changed_items:
        low, high, unit = nrc[item]
        
        val_old = per1k(final_old[item])
        val_new = per1k(final_new[item])
        
        ok_old = val_old >= low
        ok_new = val_new >= low
        if ok_old: old_pass += 1
        if ok_new: new_pass += 1
        
        ratio_old = val_old / low if low > 0 else float('inf')
        ratio_new = val_new / low if low > 0 else float('inf')
        
        flag = "✅" if ok_new else "❌"
        
        print(f"  {item:<8} {low:>10.1f} {val_old:>12.2f} {ratio_old:>7.1f}× {val_new:>12.2f} {ratio_new:>7.1f}× {flag:>6}")
    
    print(f"  变更项: 旧版 {old_pass}/{len(changed_items)} 通过, 新版 {new_pass}/{len(changed_items)} 通过")

# ═══════════════════════════════════════════════════════
# 第三部分：完整 29/29 校验（新版）
# ═══════════════════════════════════════════════════════
print("\n\n" + "=" * 80)
print("第三部分：新版 (2/0.5/0.5/0.5/0.5) 完整 29/29 校验")
print("=" * 80)

all_items = list(nrc.keys())

for vname in ['A', 'B', 'C']:
    amounts = versions[vname]
    food_new, final_new, kcal = calc_version(amounts, NEW)
    per1k = lambda x: x / kcal * 1000
    
    passed = 0
    failed = []
    print(f"\n─── {vname}版 (kcal={kcal:.0f}) ───")
    print(f"  {'指标':<10} {'值/1000k':>12} {'NRC下限':>10} {'NRC上限':>10} {'结果':>6}")
    
    for item in all_items:
        low, high, unit = nrc[item]
        val = per1k(final_new[item])
        ok = val >= low and (high is None or val <= high)
        if ok:
            passed += 1
        else:
            failed.append(item)
        flag = "✅" if ok else "❌"
        high_str = f"{high:.0f}" if high else "—"
        print(f"  {item:<10} {val:>12.2f} {low:>10.1f} {high_str:>10} {flag:>6}")
    
    ca_p = final_new['钙'] / final_new['磷']
    print(f"  Ca:P = {ca_p:.3f}")
    print(f"  结果: {passed}/29 {'✅ 全部通过' if passed == 29 else '❌ 未通过: ' + ', '.join(failed)}")

# ═══════════════════════════════════════════════════════
# 第四部分：旧版完整 29/29 校验（确认旧版也通过）
# ═══════════════════════════════════════════════════════
print("\n\n" + "=" * 80)
print("第四部分：旧版 (8/2/1/1/1) 完整 29/29 校验")
print("=" * 80)

for vname in ['A', 'B', 'C']:
    amounts = versions[vname]
    food_old, final_old, kcal = calc_version(amounts, OLD)
    per1k = lambda x: x / kcal * 1000
    
    passed = 0
    failed = []
    
    for item in all_items:
        low, high, unit = nrc[item]
        val = per1k(final_old[item])
        ok = val >= low and (high is None or val <= high)
        if ok:
            passed += 1
        else:
            failed.append(item)
    
    print(f"  {vname}版: {passed}/29 {'✅ 全部通过' if passed == 29 else '❌ 未通过: ' + ', '.join(failed)}")

# ═══════════════════════════════════════════════════════
# 第五部分：旧版冗余度排行（按 实际/NRC 倍率排序）
# ═══════════════════════════════════════════════════════
print("\n\n" + "=" * 80)
print("第五部分：旧版冗余度排行 —— C版（最常用）")
print("以 实际值/NRC下限 倍率降序排列，看哪些补剂浪费最多")
print("=" * 80)

amounts = versions['C']
food_old, final_old, kcal = calc_version(amounts, OLD)
per1k_c = lambda x: x / kcal * 1000

rows = []
for item in all_items:
    low, high, unit = nrc[item]
    val = per1k_c(final_old[item])
    ratio = val / low if low > 0 else float('inf')
    rows.append((item, val, low, ratio, unit))

rows.sort(key=lambda x: -x[3])
print(f"\n  {'指标':<12} {'值/1000k':>12} {'NRC下限':>10} {'倍率':>8} 单位")
print(f"  {'─'*55}")
for item, val, low, ratio, unit in rows:
    bar = "█" * min(int(ratio), 40)
    print(f"  {item:<12} {val:>12.1f} {low:>10.1f} {ratio:>7.1f}× {bar}")

# ═══════════════════════════════════════════════════════
# 第六部分：关键结论 —— 旧算法到底"错"在哪
# ═══════════════════════════════════════════════════════
print("\n\n" + "=" * 80)
print("第六部分：结论汇总")
print("=" * 80)

print("""
旧算法本身计算没有"错"——optimize_supplements.py 的 NRC 最低需求计算是正确的。
问题出在"从最低需求到最终用量"的决策环节：

  旧的处理方式是：
    - optimize_supplements.py 正确计算出 NRC 最低需求
    - 但最终文档选用量时，VE/B-50/锌/铁/锰全部取整到"整粒/整片"
    - 而且 VE 还额外按"鱼油:VE=1:0.8mg"的民间比例加了大量余量
    - B-50 也按"反正便宜加两片保险"的逻辑取了远超 NRC 的量

  新的处理方式是：
    - 同样的 NRC 最低需求计算
    - 允许半粒/半片操作（折半研碎）
    - VE 不再追求"鱼油配比"民间比例，只保证 NRC 3× 余量
    - B-50 食物已远超 NRC，0.5 片纯兜底
""")

# 量化：旧版 C 版 VE 的冗余
food_c, final_c_old, kcal_c = calc_version(versions['C'], OLD)
_, final_c_new, _ = calc_version(versions['C'], NEW)
ve_nrc_need = 10 * kcal_c / 1000  # mg per batch
ve_food = food_c['VE']
ve_old_supp = 8 * 100 * 0.6711
ve_new_supp = 2 * 100 * 0.6711
print(f"  VE 具体数据 (C版):")
print(f"    NRC需求(整批): {ve_nrc_need:.1f} mg")
print(f"    食物VE:         {ve_food:.1f} mg")
print(f"    旧补充(8粒):    {ve_old_supp:.1f} mg → 总计 {ve_food+ve_old_supp:.1f} mg → {(ve_food+ve_old_supp)/ve_nrc_need:.1f}× NRC")
print(f"    新补充(2粒):    {ve_new_supp:.1f} mg → 总计 {ve_food+ve_new_supp:.1f} mg → {(ve_food+ve_new_supp)/ve_nrc_need:.1f}× NRC")

b_items_detail = [('VB1', 50), ('VB2', 50), ('VB3', 50), ('VB6', 50), ('VB12', 50), ('叶酸', 400), ('泛酸', 50)]
print(f"\n  B-50 具体数据 (C版, kcal={kcal_c:.0f}):")
r_c = kcal_c / 1000
for bname, per_pill in b_items_detail:
    low, _, unit = nrc[bname]
    need = low * r_c
    food_val = food_c[bname]
    old_total = food_val + 2 * per_pill
    new_total = food_val + 0.5 * per_pill
    print(f"    {bname:<6}: NRC需={need:>8.2f}  食物={food_val:>8.2f}  "
          f"旧(+2片)={old_total:>8.1f} ({old_total/need:.0f}×)  "
          f"新(+0.5片)={new_total:>8.1f} ({new_total/need:.0f}×)")
