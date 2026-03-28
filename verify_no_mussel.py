import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ====== 新配方：删除青口贝，用Source Naturals锰片替代 ======
# 青口贝3%重新分配：鸡腿肉+1%, 猪瘦肉+1%, 鸡心+1%

# ---- 食材用量(g) ----
ingredients = {
    #            用量g  kcal/100g  蛋白g  脂肪g  磷mg  钙mg  铁mg   锌mg   铜mg    锰mg    碘mcg  硒mcg  VA_IU   VD_IU  VE_mg  VB1mg  VB2mg  VB3mg  VB6mg  VB12mcg 牛磺酸mg AA_mg
    '鸡腿肉':  [825,   119,      19.6,  4.3,  178,  9,    0.8,   1.8,   0.06,  0.02,   1,     23.0,  50,     5,     0.2,   0.07,  0.16,  5.3,   0.33,  0.4,    40,     50],
    '猪瘦肉':  [600,   143,      21.1,  6.9,  197,  5,    0.8,   1.9,   0.06,  0.01,   1,     32.5,  7,      12,    0.5,   0.81,  0.23,  5.0,   0.42,  0.6,    50,     70],
    '鸡心':    [410,   153,      15.6,  9.3,  177,  12,   5.9,   6.6,   0.33,  0.05,   5,     16.0,  31,     0,     0.7,   0.13,  0.73,  4.8,   0.29,  7.3,    145,    84],
    '牛心':    [445,   112,      17.7,  3.9,  212,  7,    4.3,   2.4,   0.39,  0.03,   5,     21.8,  0,      0,     0.2,   0.24,  0.91,  7.4,   0.28,  8.6,    160,    25],
    '鸡蛋':    [254,   143,      12.6,  9.9,  198,  56,   1.8,   1.3,   0.07,  0.03,   27,    30.7,  520,    82,    1.1,   0.04,  0.46,  0.1,   0.14,  0.9,    20,     155],
    '鸡肝':    [130,   119,      16.9,  4.8,  297,  8,    9.0,   2.7,   0.49,  0.26,   3,     54.6,  11078,  12,    0.7,   0.31,  1.78,  9.7,   0.85,  16.6,   30,     260],
    '牛肝':    [100,   135,      20.4,  3.6,  387,  5,    4.9,   4.0,   9.76,  0.31,   3,     39.7,  16898,  49,    0.5,   0.19,  2.76,  13.2,  1.08,  59.3,   40,     200],
    '鱼':      [130,   205,      18.6,  13.9, 217,  12,   1.6,   0.6,   0.07,  0.01,   44,    44.1,  167,    360,   1.5,   0.18,  0.31,  9.1,   0.40,  8.7,    70,     60],
    # 青口贝已删除
    '鸡皮':    [285,   349,      13.3,  32.4, 68,   11,   0.7,   0.6,   0.02,  0.01,   1,     14.1,  150,    0,     0.3,   0.01,  0.07,  2.5,   0.05,  0.3,    10,     250],
}

# 列索引
IDX_AMT, IDX_KCAL, IDX_PROT, IDX_FAT, IDX_P, IDX_CA, IDX_FE, IDX_ZN, IDX_CU, IDX_MN, IDX_I, IDX_SE, IDX_VA, IDX_VD, IDX_VE, IDX_VB1, IDX_VB2, IDX_VB3, IDX_VB6, IDX_VB12, IDX_TAU, IDX_AA = range(22)

# ---- 计算食材总营养 ----
totals = [0.0] * 22
raw_total = 0
for name, vals in ingredients.items():
    amt = vals[IDX_AMT]
    raw_total += amt
    factor = amt / 100.0
    for i in range(1, 22):
        totals[i] += vals[i] * factor

total_kcal = totals[IDX_KCAL]
finished = raw_total * 0.90  # 出成率90%

print(f"原料总量: {raw_total}g")
print(f"成品重量: {finished:.0f}g")
print(f"食材总能量: {total_kcal:.0f} kcal")

# ---- 补充剂 ----
# 碳酸钙 18g → 7200mg Ca
supp_ca = 18 * 400  # mg
# 牛磺酸 3g
supp_tau = 3000  # mg
# 鱼油 10粒 × 300mg EPA+DHA
supp_epadha = 10 * 300  # mg
supp_fish_oil_kcal = 10 * 9  # ~9 kcal per capsule
# VE 2粒 × 400IU = 800IU → ~536mg (1IU = 0.67mg d-α-tocopherol)
supp_ve = 2 * 400 * 0.67  # mg
# B-50 2片
supp_vb1 = 2 * 50  # mg
supp_vb2 = 2 * 50  # mg
supp_vb3 = 2 * 50  # mg (niacin/niacinamide)
supp_vb6 = 2 * 50  # mg
supp_vb12 = 2 * 50  # mcg
# 海带碘 - 试7粒 (补偿青口贝损失的120mcg碘)
kelp_pills = 7
supp_iodine = kelp_pills * 225  # mcg
# 碘盐 3g (25mcg/g)
supp_iodine_salt = 3 * 25  # mcg
# 锌片 2粒 × 15mg
supp_zn = 2 * 15  # mg
# 螯合铁 2粒 × 18mg (删除青口贝后铁略不足，增至2粒)
supp_fe = 2 * 18  # mg
# Source Naturals锰片 1粒 × 10mg
supp_mn = 1 * 10  # mg

total_kcal_with_supp = total_kcal + supp_fish_oil_kcal

print(f"总能量(含鱼油): {total_kcal_with_supp:.0f} kcal")
print(f"能量密度: {total_kcal_with_supp / finished:.3f} kcal/g")
print()

# ---- 汇总各营养素(per 1000 kcal) ----
k = total_kcal_with_supp

def per1k(val):
    return val / k * 1000

# 蛋白质
prot = totals[IDX_PROT]
fat = totals[IDX_FAT]
phosphorus = totals[IDX_P]
calcium_food = totals[IDX_CA]
calcium_total = calcium_food + supp_ca
iron_food = totals[IDX_FE]
iron_total = iron_food + supp_fe
zinc_food = totals[IDX_ZN]
zinc_total = zinc_food + supp_zn
copper = totals[IDX_CU]
mn_food = totals[IDX_MN]
mn_total = mn_food + supp_mn
iodine_food = totals[IDX_I]
iodine_total = iodine_food + supp_iodine + supp_iodine_salt
selenium = totals[IDX_SE]
va = totals[IDX_VA]
vd = totals[IDX_VD]
ve_food = totals[IDX_VE]
ve_total_mg = ve_food + supp_ve
vb1_food = totals[IDX_VB1]
vb1_total = vb1_food + supp_vb1
vb2_food = totals[IDX_VB2]
vb2_total = vb2_food + supp_vb2
vb3_food = totals[IDX_VB3]
vb3_total = vb3_food + supp_vb3
vb6_food = totals[IDX_VB6]
vb6_total = vb6_food + supp_vb6
vb12_food = totals[IDX_VB12]
vb12_total = vb12_food + supp_vb12
taurine_food = totals[IDX_TAU]
taurine_cooked = taurine_food * 0.4  # 60% cooking loss
taurine_total = taurine_cooked + supp_tau
aa = totals[IDX_AA]
epadha = supp_epadha  # mostly from supplement

# NRC RA (per 1000 kcal) for adult cats
nrc = {
    '蛋白质(g)':     (50,    None,    per1k(prot)),
    '脂肪(g)':       (22.5,  None,    per1k(fat)),
    '钙(mg)':        (720,   3000,    per1k(calcium_total)),
    '磷(mg)':        (640,   None,    per1k(phosphorus)),
    '铁(mg)':        (20,    None,    per1k(iron_total)),
    '锌(mg)':        (18.5,  None,    per1k(zinc_total)),
    '铜(mg)':        (1.2,   None,    per1k(copper)),
    '锰(mg)':        (1.2,   None,    per1k(mn_total)),
    '碘(mcg)':       (350,   9000,    per1k(iodine_total)),
    '硒(mcg)':       (75,    None,    per1k(selenium)),
    '牛磺酸(mg)':    (250,   None,    per1k(taurine_total)),
    'VA(IU)':        (3333,  333333,  per1k(va)),
    'VD(IU)':        (70,    7500,    per1k(vd)),
    'VE(mg)':        (10,    None,    per1k(ve_total_mg)),
    'VB1(mg)':       (1.4,   None,    per1k(vb1_total)),
    'VB2(mg)':       (1.0,   None,    per1k(vb2_total)),
    'VB3(mg)':       (10,    None,    per1k(vb3_total)),
    'VB6(mg)':       (0.625, None,    per1k(vb6_total)),
    'VB12(mcg)':     (5.6,   None,    per1k(vb12_total)),
    '花生四烯酸(mg)':(15,    None,    per1k(aa)),
}

pass_count = 0
fail_count = 0
print(f"{'营养素':<18} {'NRC最低':>10} {'NRC上限':>10} {'本配方':>10}  状态")
print("-" * 70)
for name, (lo, hi, val) in nrc.items():
    ok = val >= lo and (hi is None or val <= hi)
    status = "✅" if ok else "❌"
    if ok:
        pass_count += 1
    else:
        fail_count += 1
    hi_str = f"{hi:>10.0f}" if hi else "       —"
    print(f"{name:<18} {lo:>10.1f} {hi_str} {val:>10.1f}  {status}")

print()

# 钙磷比
cap = calcium_total / phosphorus
print(f"Ca:P = {calcium_total:.0f}/{phosphorus:.0f} = {cap:.3f} → {'✅' if 1.1 <= cap <= 1.5 else '❌'}")

# 牛磺酸/kg
tau_per_kg = taurine_total / (finished / 1000)
print(f"牛磺酸/kg成品 = {tau_per_kg:.0f} mg/kg → {'✅' if tau_per_kg >= 1000 else '❌'} ≥1000")

# EPA+DHA
print(f"EPA+DHA = {epadha}mg（补充剂）+ 鱼类天然含量")

# 锰详细
print(f"\n锰详细: 食材={mn_food:.2f}mg + Source Naturals={supp_mn}mg → 总计{mn_total:.2f}mg → {per1k(mn_total):.2f}/1000kcal")
# 铁详细
print(f"铁详细: 食材={iron_food:.2f}mg + 螯合铁={supp_fe}mg → 总计{iron_total:.2f}mg → {per1k(iron_total):.2f}/1000kcal")
# 碘详细
print(f"碘详细: 食材={iodine_food:.1f}mcg + 海带碘{kelp_pills}粒={supp_iodine}mcg + 碘盐={supp_iodine_salt}mcg → 总计{iodine_total:.1f}mcg → {per1k(iodine_total):.1f}/1000kcal")

# 每只猫能量
print(f"\n每只猫能量计算:")
cat_a = 30 * 4.0 + 60 * (total_kcal_with_supp / finished)
cat_b = 30 * 4.0 + 50 * (total_kcal_with_supp / finished)
cat_c = 40 * 4.0 + 80 * (total_kcal_with_supp / finished)
print(f"  公猫A = {cat_a:.0f}kcal, 母猫B = {cat_b:.0f}kcal, 幼猫C = {cat_c:.0f}kcal, 合计 = {cat_a+cat_b+cat_c:.0f}kcal")

print(f"\n{'✅' if fail_count == 0 else '❌'} {pass_count}/{pass_count+fail_count} 项NRC指标达标{'！' if fail_count == 0 else f'，{fail_count}项不达标'}")
