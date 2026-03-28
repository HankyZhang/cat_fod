"""
检查：往 C版（鸭胸强化+鲅鱼）里加入啤酒酵母后，29项NRC是否仍然达标。
啤酒酵母数据来源：USDA FoodData Central — Yeast, brewer's, dried (per 100g)
"""

# ── 啤酒酵母营养数据 (per 100g, dried) ──
yeast = {
    "kcal":       325,
    "protein":    49.0,   # g
    "fat":        3.9,    # g
    "calcium":    30,     # mg
    "phosphorus": 1200,   # mg  ← 这是最关键的
    "potassium":  955,    # mg
    "sodium":     51,     # mg
    "chloride":   0,      # mg (negligible)
    "magnesium":  54,     # mg
    "iron":       2.5,    # mg
    "zinc":       3.5,    # mg
    "copper":     0.45,   # mg
    "manganese":  0.31,   # mg
    "iodine":     0,      # mcg (negligible)
    "selenium":   7.0,    # mcg
    "taurine":    0,      # mg
    "VA":         0,      # IU
    "VD":         0,      # IU
    "VE":         0.09,   # mg α-TE
    "VB1":        11.0,   # mg
    "VB2":        4.0,    # mg
    "VB3":        40.0,   # mg
    "VB6":        4.4,    # mg
    "VB12":       0.01,   # mcg (brewer's yeast has very little B12)
    "choline":    32,     # mg
    "folate":     2340,   # mcg
    "pantothenic":5.1,    # mg
    "AA":         0,      # mg
    "EPA_DHA":    0,      # mg
    "linoleic":   0,      # g
}

# ── C版（鸭胸强化+鲅鱼）基线值 (per 1000 kcal) ──
# 来自 calc_all_spanish_versions.py 的精确输出
c_base_per1000 = {
    "protein":    116.3,
    "fat":        52.7,
    "calcium":    1616.1,
    "phosphorus": 1303.6,
    "potassium":  1615.4,
    "sodium":     814.6,
    "chloride":   385.2,
    "magnesium":  128.7,
    "iron":       27.2,
    "zinc":       22.8,
    "copper":     3.3,
    "manganese":  2.4,
    "iodine":     387.3,
    "selenium":   145.3,
    "taurine":    785.7,
    "VA":         6887.2,
    "VD":         152.4,
    "VE":         117.2,
    "VB1":        22.4,
    "VB2":        25.1,
    "VB3":        57.8,
    "VB6":        23.4,
    "VB12":       55.9,
    "choline":    742.1,
    "folate":     494.3,
    "pantothenic":33.1,
    "AA":         485.7,
    "EPA_DHA":    888.0,
    "linoleic":   9.3,
}
c_base_kcal = 4724.3  # 整锅总热量

# ── NRC 2006 成猫推荐量 (per 1000 kcal ME) ──
nrc = {
    "protein":    (50, "g"),
    "fat":        (22.5, "g"),
    "calcium":    (720, "mg"),
    "phosphorus": (640, "mg"),
    "potassium":  (1300, "mg"),
    "sodium":     (170, "mg"),
    "chloride":   (240, "mg"),
    "magnesium":  (120, "mg"),
    "iron":       (20, "mg"),
    "zinc":       (18.5, "mg"),
    "copper":     (1.2, "mg"),
    "manganese":  (1.2, "mg"),
    "iodine":     (350, "mcg"),
    "selenium":   (75, "mcg"),
    "taurine":    (100, "mg"),
    "VA":         (833, "IU"),
    "VD":         (70, "IU"),
    "VE":         (10, "mg"),
    "VB1":        (1.4, "mg"),
    "VB2":        (1.0, "mg"),
    "VB3":        (10, "mg"),
    "VB6":        (0.625, "mg"),
    "VB12":       (5.6, "mcg"),
    "choline":    (637, "mg"),
    "folate":     (188, "mcg"),
    "pantothenic":(1.44, "mg"),
    "AA":         (15, "mg"),
    "EPA_DHA":    (25, "mg"),
    "linoleic":   (1.4, "g"),
}

print("=" * 72)
print("啤酒酵母添加量 vs 29项NRC校验（C版 鸭胸强化+鲅鱼）")
print("=" * 72)

for grams in [10, 15, 20, 25, 30, 40, 50]:
    # 计算添加的绝对营养量
    add_kcal = yeast["kcal"] * grams / 100
    new_total_kcal = c_base_kcal + add_kcal

    # 把原基线值还原成绝对量，再加上酵母的绝对量，再除以新总热量
    passed = 0
    failed_items = []
    cap_ratio = None

    for nutrient, (nrc_min, unit) in nrc.items():
        # 原绝对量
        base_abs = c_base_per1000[nutrient] * c_base_kcal / 1000
        # 酵母绝对量
        yeast_abs = yeast.get(nutrient, 0) * grams / 100
        # 新 per 1000 kcal
        new_per1000 = (base_abs + yeast_abs) / new_total_kcal * 1000

        if nutrient == "calcium":
            ca_per1000 = new_per1000
        if nutrient == "phosphorus":
            p_per1000 = new_per1000

        if new_per1000 >= nrc_min:
            passed += 1
        else:
            failed_items.append(f"  {nutrient}: {new_per1000:.1f} < {nrc_min} {unit}")

    cap_ratio = ca_per1000 / p_per1000 if p_per1000 > 0 else 0

    status = "✅ 29/29" if passed == 29 else f"❌ {passed}/29"
    print(f"\n添加 {grams}g 啤酒酵母:")
    print(f"  总热量: {new_total_kcal:.0f} kcal | Ca:P = {cap_ratio:.3f} | {status}")
    if failed_items:
        for f in failed_items:
            print(f)

    # 额外输出关键指标变化
    base_cap = c_base_per1000["calcium"] / c_base_per1000["phosphorus"]
    print(f"  Ca:P 变化: {base_cap:.3f} → {cap_ratio:.3f}")

# ── 推荐用量区间的详细营养表 ──
print("\n" + "=" * 72)
print("推荐用量 20g 的完整营养明细")
print("=" * 72)
grams = 20
add_kcal = yeast["kcal"] * grams / 100
new_total_kcal = c_base_kcal + add_kcal
print(f"总热量: {new_total_kcal:.1f} kcal")
print(f"能量密度: {new_total_kcal / 2851:.3f} kcal/g")
print(f"每天三猫合计 (190g 猫饭): {190 * new_total_kcal / 2851 + 100 * 3.8:.0f} kcal\n")

print(f"{'营养素':<14} {'原值/1000kcal':>14} {'加酵母后':>14} {'NRC最低':>10} {'状态':>6}")
print("-" * 62)
for nutrient, (nrc_min, unit) in nrc.items():
    base_abs = c_base_per1000[nutrient] * c_base_kcal / 1000
    yeast_abs = yeast.get(nutrient, 0) * grams / 100
    new_per1000 = (base_abs + yeast_abs) / new_total_kcal * 1000
    ok = "✅" if new_per1000 >= nrc_min else "❌"
    print(f"{nutrient:<14} {c_base_per1000[nutrient]:>14.1f} {new_per1000:>14.1f} {nrc_min:>10} {ok}")

ca_abs = c_base_per1000["calcium"] * c_base_kcal / 1000 + yeast["calcium"] * grams / 100
p_abs = c_base_per1000["phosphorus"] * c_base_kcal / 1000 + yeast["phosphorus"] * grams / 100
print(f"\nCa:P = {ca_abs/p_abs:.3f}")
