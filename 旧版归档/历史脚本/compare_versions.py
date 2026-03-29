# -*- coding: utf-8 -*-
"""
历史版本对比脚本（归档保留）

比较对象是旧 9% 鸡皮 / 旧 A-B-C 版本，数值已不是现行鲅鱼总版口径。
仅用于查看早期演化过程。
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

versions = {
    '原始9%鸡皮': {'kcal': 4954, 'density': 1.737, 'cap': 1.257, 'skin': 285, 'chicken': 825, 'pork': 600, 'duck': 0},
    'A_7%鸡皮':   {'kcal': 4809, 'density': 1.687, 'cap': 1.243, 'skin': 222, 'chicken': 888, 'pork': 600, 'duck': 0},
    'B_鸭胸600g': {'kcal': 4761, 'density': 1.670, 'cap': 1.241, 'skin': 222, 'chicken': 888, 'pork': 0, 'duck': 600},
    'C_鸭胸900g': {'kcal': 4809, 'density': 1.687, 'cap': 1.227, 'skin': 222, 'chicken': 588, 'pork': 0, 'duck': 900},
}

print('=' * 80)
print('四个版本全面对比')
print('=' * 80)
for name, v in versions.items():
    daily_a = 30*4.0 + 60*v['density']
    daily_b = 30*4.0 + 50*v['density']
    daily_c = 40*4.0 + 80*v['density']
    total = daily_a + daily_b + daily_c
    skin = v['skin']
    chk = v['chicken']
    prk = v['pork']
    dck = v['duck']
    kcal = v['kcal']
    dens = v['density']
    cap = v['cap']
    print(f'{name}: {kcal} kcal, {dens:.3f}/g, Ca:P={cap:.3f}')
    print(f'  skin={skin}g, chicken={chk}g, pork={prk}g, duck={dck}g')
    print(f'  daily: A={daily_a:.0f} B={daily_b:.0f} C={daily_c:.0f} total={total:.0f} kcal')
    print()

# 关键"薄弱环节"营养素余量
print('=' * 80)
print('关键营养素余量对比（越大越安全）')
print('=' * 80)

# 碘 (最薄弱项)
print('\n碘 (NRC RA=350 mcg/1000kcal):')
for name, val in [('原始9%', 371.6), ('A版', 382.8), ('B版', 386.7), ('C版', 382.8)]:
    margin = (val - 350) / 350 * 100
    print(f'  {name}: {val:.1f}  余量={margin:.1f}%')

# 花生四烯酸 (鸭胸按0计，受影响最大)
print('\n花生四烯酸 (NRC RA=15 mg/1000kcal, 鸭胸按0保守计):')
for name, val in [('原始9%', 603.8), ('A版', 595.7), ('B版', 513.5), ('C版', 477.2)]:
    margin = (val - 15) / 15 * 100
    print(f'  {name}: {val:.1f}  余量={margin:.0f}%  (即使保守计仍为NRC最低值的{val/15:.0f}倍)')

# 牛磺酸
print('\n牛磺酸 (NRC RA=250 mg/1000kcal):')
for name, val in [('原始9%', 781.7), ('A版', 806.9), ('B版', 789.8), ('C版', 771.9)]:
    margin = (val - 250) / 250 * 100
    print(f'  {name}: {val:.1f}  余量={margin:.0f}%')

# 胆碱 (C版计算值和文档值有偏差，确认是否仍达标)
print('\n胆碱 (NRC RA=637 mg/1000kcal):')
for name, val in [('原始9%', 725.3), ('A版', 749.6), ('B版', 723.9), ('C版', 709.6)]:
    margin = (val - 637) / 637 * 100
    print(f'  {name}: {val:.1f}  余量={margin:.1f}%')

# 每日热量满足度
print('\n' + '=' * 80)
print('每日热量满足度（目标: A~220-250, B~200-220, C~280-300）')
print('=' * 80)
for name, v in versions.items():
    da = 30*4.0 + 60*v['density']
    db = 30*4.0 + 50*v['density']
    dc = 40*4.0 + 80*v['density']
    print(f'{name}: A={da:.0f}kcal B={db:.0f}kcal C={dc:.0f}kcal  total={da+db+dc:.0f}kcal/day')
