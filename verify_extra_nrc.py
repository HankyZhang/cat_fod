# -*- coding: utf-8 -*-
"""
补充验证：NRC 2006 中当前主脚本未覆盖的 5 项必需营养素
氯化物(Cl)、镁(Mg)、胆碱(Choline)、叶酸(Folate)、泛酸(Pantothenic acid)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ========== 食材用量 ==========
amounts = {
    '鸡腿肉': 825, '猪瘦肉': 600, '鸡心': 410, '牛心': 445,
    '鸡蛋': 254, '鸡肝': 127, '牛肝': 95, '鱼': 127, '鸡皮': 285,
}
vals = list(amounts.values())
total_raw = sum(vals)
finished = total_raw * 0.9

def total(arr):
    return sum(v/100 * a for v, a in zip(vals, arr))

# ========== USDA 每100g 数据（Atlantic mackerel 口径） ==========

# 镁 mg/100g  — USDA Standard Reference
mg_per100 = [23, 25, 15, 21, 12, 19, 20, 76, 10]
# 鸡腿肉≈23, 猪瘦肉≈25, 鸡心≈15, 牛心≈21, 鸡蛋≈12, 鸡肝≈19, 牛肝≈20, Atlantic mackerel≈76, 鸡皮≈10

# 胆碱 mg/100g — USDA
choline_per100 = [65, 80, 65, 150, 293, 290, 333, 65, 46]
# 鸡腿肉≈65, 猪瘦肉≈80, 鸡心≈65, 牛心≈150, 鸡蛋≈293, 鸡肝≈290, 牛肝≈333, 鲭鱼≈65, 鸡皮≈46

# 叶酸 mcg/100g — USDA (DFE)
folate_per100 = [6, 1, 72, 3, 47, 588, 290, 1, 1]
# 鸡腿肉≈6, 猪瘦肉≈1, 鸡心≈72, 牛心≈3, 鸡蛋≈47, 鸡肝≈588, 牛肝≈290, 鲭鱼≈1, 鸡皮≈1

# 泛酸 mg/100g — USDA
panto_per100 = [1.01, 0.60, 2.51, 2.25, 1.53, 6.50, 7.17, 0.86, 0.53]
# 鸡腿肉≈1.01, 猪瘦肉≈0.60, 鸡心≈2.51, 牛心≈2.25, 鸡蛋≈1.53, 鸡肝≈6.50, 牛肝≈7.17, 鲭鱼≈0.86, 鸡皮≈0.53

# ========== 补充剂 ==========
# 碘盐 3g NaCl → 氯 = 3000 * 0.6066 = 1819.8 mg
salt_cl = 3000 * 0.6066

# B-50 复合片(2片)中典型含量：
#   叶酸 ~400 mcg/片 → 800 mcg
#   泛酸 ~50 mg/片 → 100 mg
#   胆碱 一般不在 B-50 中
supp_folate = 800   # mcg
supp_panto  = 100   # mg
supp_choline = 0    # mg  (B-50 通常不含胆碱)

# ========== 鱼油 10 粒总热量 ==========
fish_oil_kcal = 90
kcal_food = sum(v/100*a for v,a in zip(vals, [119,143,153,112,143,119,135,205.4,349]))
kcal = kcal_food + fish_oil_kcal

per1k = lambda x: x / kcal * 1000

# ========== 计算 ==========
food_mg     = total(mg_per100)
food_chol   = total(choline_per100)
food_folate = total(folate_per100)
food_panto  = total(panto_per100)

final_cl      = salt_cl   # 食材本身的氯微量忽略
final_mg      = food_mg
final_choline = food_chol + supp_choline
final_folate  = food_folate + supp_folate
final_panto   = food_panto + supp_panto

# NRC 2006 RA per 1000 kcal (adult cat)
checks = [
    ('氯化物',   final_cl,      240,  None, 'mg'),
    ('镁',       final_mg,      100,  None, 'mg'),
    ('胆碱',     final_choline, 637,  None, 'mg'),
    ('叶酸',     final_folate,  188,  None, 'mcg'),
    ('泛酸',     final_panto,   1.44, None, 'mg'),
]

print('=' * 60)
print('补充 NRC 校验：氯化物 / 镁 / 胆碱 / 叶酸 / 泛酸')
print('=' * 60)
print(f'总能量(含鱼油): {kcal:.1f} kcal\n')

issues = []
print(f"{'营养素':<8} {'总量':>10} {'每1000kcal':>12} {'NRC最低':>10}  状态")
print('-'*56)
for name, val, low, high, unit in checks:
    p = per1k(val)
    ok = p >= low
    if not ok:
        issues.append((name, p, low))
    print(f"{name:<8} {val:>10.1f} {p:>12.1f} {low:>10g}  {'✅' if ok else '❌'}")

print()
# 详细拆解
print(f"氯化物: 碘盐3g→NaCl氯={salt_cl:.1f}mg, /1000kcal={per1k(salt_cl):.1f}")
print(f"镁: 食材={food_mg:.1f}mg, /1000kcal={per1k(food_mg):.1f}")
print(f"胆碱: 食材={food_chol:.1f}mg, 补={supp_choline}, 合计={final_choline:.1f}, /1000kcal={per1k(final_choline):.1f}")
print(f"叶酸: 食材={food_folate:.1f}mcg, 补={supp_folate}, 合计={final_folate:.1f}, /1000kcal={per1k(final_folate):.1f}")
print(f"泛酸: 食材={food_panto:.1f}mg, 补={supp_panto}, 合计={final_panto:.1f}, /1000kcal={per1k(final_panto):.1f}")

print()
if issues:
    print(f'⚠️ 未达标: {len(issues)} 项')
    for row in issues:
        print(f'  {row[0]}: {row[1]:.1f} < {row[2]:.1f}')
else:
    print('5/5 补充项全部达标 → 合并主脚本可达 29/29')
