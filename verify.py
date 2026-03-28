# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import math

print("=" * 70)
print("  猫饭NRC优化配方 · 完整数值验证报告")
print("=" * 70)

# --------------------------------------------------
# 1. 基础参数
# --------------------------------------------------
print("\n【1】基础参数验证")
print("-" * 50)

cats = [
    ("公猫A", 5.8, 1.0, "成猫偏胖，减重系数"),
    ("母猫B", 4.5, 1.0, "成猫正常，维持"),
    ("幼猫C", 2.5, 1.8, "幼猫，生长期"),
]

total_energy = 0
for name, bw, factor, note in cats:
    rer = 70 * (bw ** 0.75)
    daily_e = rer * factor
    total_energy += daily_e
    print(f"  {name}: BW={bw}kg, RER={rer:.1f} kcal, x{factor} -> {daily_e:.0f} kcal/天 ({note})")

print(f"  -> 三只猫总能量需求 = {total_energy:.0f} kcal/天")

kibble_kcal_per_g = 4.0
catfood_total = 190 * 15  # 2850g
yield_rate = 0.90

kibble_actual = 115
catfood_kcal_est = 190 * 1.1
print(f"\n  干粮分配: 40+40+35={kibble_actual}g = {kibble_actual * kibble_kcal_per_g:.0f} kcal")
print(f"  猫饭分配: 60+50+80=190g ≈ {catfood_kcal_est:.0f} kcal")
print(f"  总计: {kibble_actual * kibble_kcal_per_g + catfood_kcal_est:.0f} kcal vs 需求{total_energy:.0f} kcal")

# --------------------------------------------------
# 2. 食材用量
# --------------------------------------------------
print("\n\n【2】食材用量验证")
print("-" * 50)

raw_total = catfood_total / yield_rate
print(f"  成品: {catfood_total}g, 出成率: {yield_rate*100:.0f}%, 原料: {raw_total:.0f}g")

amounts = {
    "鸡腿肉": 800, "猪瘦肉": 570, "鸡心": 380, "牛心": 450,
    "鸡蛋": 254, "鸡肝": 130, "牛肝": 100, "鱼": 130,
    "青口贝": 100, "鸡皮": 285,
}
total_raw = sum(amounts.values())
print(f"  实际食材总量: {total_raw}g (理论{raw_total:.0f}g, 差{total_raw - raw_total:.0f}g)")

ratios = {"鸡腿肉": 0.25, "猪瘦肉": 0.18, "鸡心": 0.12, "牛心": 0.14,
          "鸡蛋": 0.08, "鸡肝": 0.04, "牛肝": 0.03, "鱼": 0.04,
          "青口贝": 0.03, "鸡皮": 0.09}

for name in amounts:
    expected = ratios[name] * raw_total
    actual = amounts[name]
    diff = actual - expected
    print(f"  {name}: 理论{expected:.0f}g, 实际{actual}g, 差{diff:+.0f}g")

# --------------------------------------------------
# 3. 营养精确计算
# --------------------------------------------------
print("\n\n【3】营养素精确计算")
print("-" * 50)

names_list = ["鸡腿肉", "猪瘦肉", "鸡心", "牛心", "鸡蛋", "鸡肝", "牛肝", "鱼", "青口贝", "鸡皮"]
amts = [amounts[n] for n in names_list]

# 每100g营养数据
data = {
    "能量kcal":       [119,   143,   153,   112,   143,   119,   135,   205,    86,   349],
    "蛋白质g":        [19.6,  21.1,  15.6,  17.7,  12.6,  16.9,  20.4,  18.6,  11.9,  13.3],
    "脂肪g":          [4.3,   6.9,   9.3,   3.9,   9.9,   4.8,   3.6,   13.9,   2.2,  32.4],
    "磷mg":           [178,   197,   177,   212,   198,   297,   387,   217,   197,    68],
    "钙mg":           [9,     5,     12,    7,     56,    8,     5,     12,    33,     11],
    "铁mg":           [0.8,   0.8,   5.9,   4.3,   1.8,   9.0,   4.9,   1.6,   3.4,   0.7],
    "锌mg":           [1.8,   1.9,   6.6,   2.4,   1.3,   2.7,   4.0,   0.6,   1.5,   0.6],
    "铜mg":           [0.06,  0.06,  0.33,  0.39,  0.07,  0.49,  9.76,  0.07,  0.07,  0.02],
    "锰mg":           [0.02,  0.01,  0.05,  0.03,  0.03,  0.26,  0.31,  0.01,  3.40,  0.01],
    "碘mcg":          [1,     1,     5,     5,     27,    3,     3,     44,    120,    1],
    "硒mcg":          [23.0,  32.5,  16.0,  21.8,  30.7,  54.6,  39.7,  44.1,  44.8,  14.1],
    "VA_IU":          [50,    7,     31,    0,     520,   11078, 16898, 167,   91,    150],
    "VD_IU":          [5,     12,    0,     0,     82,    12,    49,    360,   0,      0],
    "VE_mg":          [0.2,   0.5,   0.7,   0.2,   1.1,   0.7,   0.5,   1.5,   0.9,   0.3],
    "VB1mg":          [0.07,  0.81,  0.13,  0.24,  0.04,  0.31,  0.19,  0.18,  0.16,  0.01],
    "VB2mg":          [0.16,  0.23,  0.73,  0.91,  0.46,  1.78,  2.76,  0.31,  0.21,  0.07],
    "VB3mg":          [5.3,   5.0,   4.8,   7.4,   0.1,   9.7,   13.2,  9.1,   1.6,   2.5],
    "VB6mg":          [0.33,  0.42,  0.29,  0.28,  0.14,  0.85,  1.08,  0.40,  0.08,  0.05],
    "VB12mcg":        [0.4,   0.6,   7.3,   8.6,   0.9,   16.6,  59.3,  8.7,   12.0,  0.3],
    "牛磺酸mg":       [40,    50,    145,   160,   20,    30,    40,    70,    100,    10],
    "花生四烯酸mg":   [50,    70,    84,    25,    155,   260,   200,   60,    20,    250],
}

totals = {}
for nutrient, values in data.items():
    t = sum(amts[i] / 100 * values[i] for i in range(10))
    totals[nutrient] = t

total_kcal = totals["能量kcal"]
per1000 = total_kcal / 1000

print(f"  总能量(原料): {total_kcal:.1f} kcal")
print(f"  能量密度: {total_kcal / catfood_total:.3f} kcal/g (成品)")

print("\n  --- 食材营养贡献明细 ---")
for nutrient in ["蛋白质g", "脂肪g", "磷mg", "钙mg", "铁mg", "锌mg", "铜mg", "锰mg",
                  "碘mcg", "硒mcg", "VA_IU", "VD_IU", "VE_mg",
                  "VB1mg", "VB2mg", "VB3mg", "VB6mg", "VB12mcg", "牛磺酸mg", "花生四烯酸mg"]:
    val = totals[nutrient]
    # 分解来源
    contribs = []
    for i in range(10):
        c = amts[i] / 100 * data[nutrient][i]
        if c > 0.01 * val and val > 0:  # 只显示>1%贡献的
            contribs.append(f"{names_list[i]}:{c:.1f}")
    top3 = sorted([(amts[i]/100*data[nutrient][i], names_list[i]) for i in range(10)], reverse=True)[:3]
    top3_str = " | ".join(f"{n}={v:.1f}" for v, n in top3)
    print(f"  {nutrient:<14}: 总={val:>10.1f}  前3: {top3_str}")

# --------------------------------------------------
# 4. 添加补充剂
# --------------------------------------------------
print("\n\n【4】添加补充剂后最终营养")
print("-" * 50)

# 补充剂
ca_supp = 18 * 400  # 碳酸钙18g, 含钙40%, = 7200mg
zn_supp = 30  # 2粒x15mg
ve_supp_mg = 800 * 0.67  # 2粒x400IU, d-alpha 1IU=0.67mg = 536mg
vb1_supp = 100  # B50 x 2片
vb2_supp = 100
vb3_supp = 100
vb6_supp = 100
vb12_supp = 100  # mcg
iodine_supp = 900 + 3 * 25  # 海带4粒 + 碘盐3g(保守25mcg/g)
tau_supp = 3000  # mg

final = dict(totals)  # copy
final["钙mg"] = totals["钙mg"] + ca_supp
final["锌mg"] = totals["锌mg"] + zn_supp
final["VE_mg"] = totals["VE_mg"] + ve_supp_mg
final["VB1mg"] = totals["VB1mg"] + vb1_supp
final["VB2mg"] = totals["VB2mg"] + vb2_supp
final["VB3mg"] = totals["VB3mg"] + vb3_supp
final["VB6mg"] = totals["VB6mg"] + vb6_supp
final["VB12mcg"] = totals["VB12mcg"] + vb12_supp
final["碘mcg"] = totals["碘mcg"] + iodine_supp

# 牛磺酸: 食材60%损失 + 补充
tau_food_after_cook = totals["牛磺酸mg"] * 0.4
tau_total = tau_food_after_cook + tau_supp
final["牛磺酸mg"] = tau_total

# --------------------------------------------------
# 5. NRC 对照
# --------------------------------------------------
print("\n\n【5】NRC 2006 成猫 RA 逐项验证 (per 1000 kcal)")
print("=" * 70)

# (NRC_min_per_1000kcal, NRC_max_per_1000kcal_or_None, key_in_final, unit)
checks = [
    ("蛋白质",     50,     None,    "蛋白质g",       "g"),
    ("脂肪",       22.5,   None,    "脂肪g",         "g"),
    ("钙",         720,    3000,    "钙mg",          "mg"),
    ("磷",         640,    None,    "磷mg",          "mg"),
    ("铁",         20,     None,    "铁mg",          "mg"),
    ("锌",         18.5,   None,    "锌mg",          "mg"),
    ("铜",         1.2,    None,    "铜mg",          "mg"),
    ("锰",         1.2,    None,    "锰mg",          "mg"),
    ("碘",         350,    9000,    "碘mcg",         "mcg"),
    ("硒",         75,     None,    "硒mcg",         "mcg"),
    ("维生素A",    3333,   333333,  "VA_IU",         "IU"),
    ("维生素D",    70,     7500,    "VD_IU",         "IU"),
    ("维生素E",    10,     None,    "VE_mg",         "mg"),
    ("维生素B1",   1.4,    None,    "VB1mg",         "mg"),
    ("维生素B2",   1.0,    None,    "VB2mg",         "mg"),
    ("维生素B3",   10,     None,    "VB3mg",         "mg"),
    ("维生素B6",   0.625,  None,    "VB6mg",         "mg"),
    ("维生素B12",  5.6,    None,    "VB12mcg",       "mcg"),
    ("牛磺酸",     250,    None,    "牛磺酸mg",      "mg"),
    ("花生四烯酸", 15,     None,    "花生四烯酸mg",  "mg"),
]

issues = []

header = f"  {'营养素':<10} {'总量':>10} {'每1000kcal':>12} {'NRC最低':>10} {'NRC上限':>10} {'状态'}"
print(header)
print("  " + "-" * 65)

for label, nrc_min, nrc_max, key, unit in checks:
    val = final.get(key, totals.get(key, 0))
    val_p1k = val / per1000
    
    status = "✅ 达标"
    if val_p1k < nrc_min:
        status = "❌ 不足"
        issues.append((label, val_p1k, nrc_min, "低于最低"))
    elif nrc_max and val_p1k > nrc_max:
        status = "❌ 超标"
        issues.append((label, val_p1k, nrc_max, "超过上限"))
    
    nmax_str = str(nrc_max) if nrc_max else "—"
    print(f"  {label:<10} {val:>10.1f}{unit:<4} {val_p1k:>10.1f} {nrc_min:>10} {nmax_str:>10} {status}")

# --------------------------------------------------
# 6. 钙磷比
# --------------------------------------------------
print(f"\n\n【6】钙磷比")
print("-" * 50)
ca = final["钙mg"]
p = totals["磷mg"]
ratio = ca / p
print(f"  Ca={ca:.0f}mg, P={p:.0f}mg, Ca:P = {ratio:.3f}")
print(f"  NRC要求: 1.1-1.5 -> {'✅' if 1.1 <= ratio <= 1.5 else '❌'}")

if ratio < 1.1 or ratio > 1.5:
    issues.append(("钙磷比", ratio, "1.1-1.5", "超出范围"))

# --------------------------------------------------
# 7. 牛磺酸
# --------------------------------------------------
print(f"\n\n【7】牛磺酸")
print("-" * 50)
print(f"  食材(生): {totals['牛磺酸mg']:.0f}mg")
print(f"  烹饪损失60%后: {totals['牛磺酸mg'] * 0.4:.0f}mg")
print(f"  补充: {tau_supp}mg")
print(f"  总: {tau_total:.0f}mg")
print(f"  /kg成品: {tau_total / (catfood_total/1000):.0f}mg/kg (需>=1000)")
print(f"  /1000kcal: {tau_total / per1000:.0f}mg (NRC RA>=250)")
tau_per_kg = tau_total / (catfood_total/1000)
print(f"  -> {'✅' if tau_per_kg >= 1000 else '❌'}")

# --------------------------------------------------
# 8. 维生素A安全
# --------------------------------------------------
print(f"\n\n【8】维生素A")
print("-" * 50)
va = totals["VA_IU"]
va_p1k = va / per1000
print(f"  总VA: {va:.0f}IU, /1000kcal: {va_p1k:.0f}")
print(f"  鸡肝贡献: {130/100*11078:.0f}IU, 牛肝贡献: {100/100*16898:.0f}IU")
print(f"  肝脏占比: {(130+100)/total_raw*100:.1f}%")
print(f"  NRC: 3333-333333/1000kcal -> {'✅' if 3333 <= va_p1k <= 333333 else '❌'}")

# --------------------------------------------------
# 9. 维生素D
# --------------------------------------------------
print(f"\n\n【9】维生素D ⚠️ 重点检查")
print("-" * 50)
vd = totals["VD_IU"]
vd_p1k = vd / per1000
print(f"  食材VD总: {vd:.1f}IU")
for i in range(10):
    c = amts[i] / 100 * data["VD_IU"][i]
    if c > 0:
        print(f"    {names_list[i]}: {c:.1f}IU")
print(f"  /1000kcal: {vd_p1k:.1f}")
print(f"  NRC最低: 70 IU/1000kcal -> {'✅' if vd_p1k >= 70 else '❌ 不足!'}")

if vd_p1k < 70:
    deficit = 70 * per1000 - vd
    print(f"  !! 缺口: {deficit:.0f}IU")
    print(f"  !! 建议: 补充维生素D3，或增加鱼比例，或依赖干粮补足")

# --------------------------------------------------
# 10. 碘
# --------------------------------------------------
print(f"\n\n【10】碘（敏感分析）")
print("-" * 50)
iod_food = totals["碘mcg"]
for salt_rate in [20, 25, 30, 75]:
    iod_salt = 3 * salt_rate
    iod_total = iod_food + 900 + iod_salt
    p1k = iod_total / per1000
    print(f"  碘盐{salt_rate}mcg/g: {iod_food:.0f}+900+{iod_salt}={iod_total:.0f}mcg -> {p1k:.0f}/1000kcal {'✅' if p1k >= 350 else '❌'}")

# --------------------------------------------------
# 11. 能量分配
# --------------------------------------------------
print(f"\n\n【11】每只猫能量")
print("-" * 50)
kcal_per_g = total_kcal / catfood_total
print(f"  猫饭: {kcal_per_g:.3f} kcal/g")
for name, kb, cf, target in [("公猫A", 40, 60, 250), ("母猫B", 40, 50, 220), ("幼猫C", 35, 80, 250)]:
    e = kb * 4.0 + cf * kcal_per_g
    print(f"  {name}: {kb}g干粮({kb*4.0:.0f}kcal) + {cf}g猫饭({cf*kcal_per_g:.0f}kcal) = {e:.0f}kcal (目标{target})")

# --------------------------------------------------
# 12. 文档 vs 计算
# --------------------------------------------------
print(f"\n\n【12】文档声称 vs 实际计算")
print("=" * 70)
checks_doc = [
    ("磷总量",           6123,   totals["磷mg"]),
    ("食材钙",           370,    totals["钙mg"]),
    ("总钙(+碳酸钙)",    7570,   final["钙mg"]),
    ("钙磷比",           1.24,   ratio),
    ("牛磺酸食材生",     1771,   totals["牛磺酸mg"]),
    ("牛磺酸/kg成品",    1300,   tau_total/(catfood_total/1000)),
    ("VA总IU",           33320,  va),
    ("VA/1000kcal",      10630,  va_p1k),
    ("蛋白质/1000kcal",  62,     totals["蛋白质g"]/per1000),
    ("脂肪/1000kcal",    35,     totals["脂肪g"]/per1000),
    ("铁/1000kcal",      27,     final["铁mg"]/per1000),
    ("锌/1000kcal",      22,     final["锌mg"]/per1000),
    ("VD/1000kcal",      200,    vd_p1k),
    ("VE/1000kcal",      90,     final["VE_mg"]/per1000),
    ("VB1/1000kcal",     2.8,    final["VB1mg"]/per1000),
    ("VB2/1000kcal",     3.2,    final["VB2mg"]/per1000),
    ("VB3/1000kcal",     25,     final["VB3mg"]/per1000),
    ("钾/1000kcal",      1500,   None),  # 没有钾数据
    ("EPA+DHA/1000kcal", 960,    None),  # 需鱼油数据
]

for label, doc_val, calc_val in checks_doc:
    if calc_val is None:
        print(f"  -- {label:<24}: 文档={doc_val:>10.1f}  (无数据验证)")
        continue
    diff = abs(doc_val - calc_val) / max(doc_val, 0.001) * 100
    st = "✅" if diff < 15 else "⚠️ 偏差大"
    print(f"  {st} {label:<24}: 文档={doc_val:>10.1f}  计算={calc_val:>10.1f}  差{diff:.1f}%")

# --------------------------------------------------
# 13. 汇总
# --------------------------------------------------
print(f"\n\n{'='*70}")
print(f"  ★ 问题汇总 ★")
print(f"{'='*70}")
if issues:
    for label, val, req, desc in issues:
        print(f"  ❌ {label}: 实际={val:.2f}, 要求={req}, {desc}")
else:
    print("  ✅ 所有NRC指标达标")

print(f"\n{'='*70}")
print("  验证完成")
print(f"{'='*70}")
