#!/usr/bin/env python3
"""
Verify nutritional data from NutritionValue.org against code values.
All data fetched from USDA via NutritionValue.org, converted to per 100g.
"""

# ============================================================
# RAW DATA FROM NUTRITIONVALUE.ORG (per serving as shown on site)
# ============================================================

data = {}

# 1. Chicken thigh (meat only, raw) - per 4.0 oz (113.0 g)
data['Chicken Thigh'] = {
    'serving_g': 113.0,
    'serving_desc': '4.0 oz (113.0 g)',
    'raw': {
        'Calories': 137,
        'Protein': 22.22,
        'Fat': 4.656,
        'Phosphorus': 209.05,
        'Calcium': 7.91,
        'Iron': 0.92,
        'Zinc': 1.79,
        'Copper': 0.07,
        'Manganese': 0.015,
        'Potassium': 273.46,
        'Sodium': 107.35,
        'Selenium': 25.88,
        'VA_RAE_mcg': 7.91,
        'VD_mcg': 0.00,
        'VE': 0.20,
        'VB1': 0.099,
        'VB2': 0.221,
        'VB3': 6.279,
        'VB6': 0.510,
        'VB12': 0.69,
        'Magnesium': 25.99,
        'Choline': 60.6,
        'Folate': 4.52,
        'Pantothenic': None,  # Not shown on page for this item
    }
}

# 2. Pork loin (tenderloin, raw) - per 4.0 oz (113.0 g)
data['Pork Loin'] = {
    'serving_g': 113.0,
    'serving_desc': '4.0 oz (113.0 g)',
    'raw': {
        'Calories': 123,
        'Protein': 23.67,
        'Fat': 2.452,
        'Phosphorus': 279.11,
        'Calcium': 5.65,
        'Iron': 1.11,
        'Zinc': 2.14,
        'Copper': 0.10,
        'Manganese': 0.017,
        'Potassium': 450.87,
        'Sodium': 59.89,
        'Selenium': 34.80,
        'VA_RAE_mcg': 0.00,
        'VD_mcg': 0.23,
        'VE': 0.25,
        'VB1': 1.128,
        'VB2': 0.386,
        'VB3': 7.553,
        'VB6': 0.878,
        'VB12': 0.58,
        'Magnesium': 30.51,
        'Choline': 91.3,
        'Folate': 0.00,
        'Pantothenic': 0.956,
    }
}

# 3. Chicken heart (raw) - per 1.0 heart (6.1 g)
data['Chicken Heart'] = {
    'serving_g': 6.1,
    'serving_desc': '1.0 heart (6.1 g)',
    'raw': {
        'Calories': 9.3,
        'Protein': 0.95,
        'Fat': 0.569,
        'Phosphorus': 10.80,
        'Calcium': 0.73,
        'Iron': 0.36,
        'Zinc': 0.40,
        'Copper': 0.02,
        'Manganese': 0.005,
        'Potassium': 10.74,
        'Sodium': 4.51,
        'Selenium': 0.26,
        'VA_RAE_mcg': 0.55,
        'VD_mcg': None,  # Not in USDA data for this item
        'VE': None,       # Not in USDA data for this item
        'VB1': 0.009,
        'VB2': 0.044,
        'VB3': 0.298,
        'VB6': 0.022,
        'VB12': 0.44,
        'Magnesium': 0.92,
        'Choline': None,  # Not in USDA data for this item
        'Folate': 4.39,
        'Pantothenic': 0.156,
    }
}

# 4. Beef heart (raw) - per 1.0 oz (28.35 g)
data['Beef Heart'] = {
    'serving_g': 28.35,
    'serving_desc': '1.0 oz (28.35 g)',
    'raw': {
        'Calories': 32,
        'Protein': 5.02,
        'Fat': 1.117,
        'Phosphorus': 60.10,
        'Calcium': 1.98,
        'Iron': 1.22,
        'Zinc': 0.48,
        'Copper': 0.11,
        'Manganese': 0.010,
        'Potassium': 81.36,
        'Sodium': 27.78,
        'Selenium': 6.18,
        'VA_RAE_mcg': 0.00,
        'VD_mcg': None,  # Not shown on page
        'VE': 0.06,
        'VB1': 0.067,
        'VB2': 0.257,
        'VB3': 2.135,
        'VB6': 0.079,
        'VB12': 2.42,
        'Magnesium': 5.95,
        'Choline': None,  # Not shown on page
        'Folate': 0.85,
        'Pantothenic': 0.507,
    }
}

# 5. Egg (whole, raw) - per 1.0 large (50.0 g)
data['Egg'] = {
    'serving_g': 50.0,
    'serving_desc': '1.0 large (50.0 g)',
    'raw': {
        'Calories': 72,
        'Protein': 6.28,
        'Fat': 4.755,
        'Phosphorus': 99.00,
        'Calcium': 28.00,
        'Iron': 0.88,
        'Zinc': 0.65,
        'Copper': 0.04,
        'Manganese': 0.014,
        'Potassium': 69.00,
        'Sodium': 71.00,
        'Selenium': 15.35,
        'VA_RAE_mcg': 80.00,
        'VD_mcg': 1.00,
        'VE': 0.53,
        'VB1': 0.020,
        'VB2': 0.229,
        'VB3': 0.037,
        'VB6': 0.085,
        'VB12': 0.45,
        'Magnesium': 6.00,
        'Choline': 146.9,
        'Folate': 23.50,
        'Pantothenic': 0.766,
    }
}

# 6. Chicken liver (raw) - per 4.0 oz (113.0 g)
data['Chicken Liver'] = {
    'serving_g': 113.0,
    'serving_desc': '4.0 oz (113.0 g)',
    'raw': {
        'Calories': 134,
        'Protein': 19.12,
        'Fat': 5.458,
        'Phosphorus': 335.61,
        'Calcium': 9.04,
        'Iron': 10.16,
        'Zinc': 3.02,
        'Copper': 0.56,
        'Manganese': 0.288,
        'Potassium': 259.90,
        'Sodium': 80.23,
        'Selenium': 61.70,
        'VA_RAE_mcg': 3724.48,
        'VD_mcg': 0.00,
        'VE': 0.79,
        'VB1': 0.345,
        'VB2': 2.009,
        'VB3': 10.993,
        'VB6': 0.964,
        'VB12': 18.74,
        'Magnesium': 21.47,
        'Choline': 219.7,
        'Folate': 664.44,
        'Pantothenic': 7.043,
    }
}

# 7. Beef liver (raw) - per 4.0 oz (113.0 g)
data['Beef Liver'] = {
    'serving_g': 113.0,
    'serving_desc': '4.0 oz (113.0 g)',
    'raw': {
        'Calories': 153,
        'Protein': 23.01,
        'Fat': 4.102,
        'Phosphorus': 437.31,
        'Calcium': 5.65,
        'Iron': 5.54,
        'Zinc': 4.52,
        'Copper': 11.02,
        'Manganese': 0.350,
        'Potassium': 353.69,
        'Sodium': 77.97,
        'Selenium': 44.86,
        'VA_RAE_mcg': 5613.84,
        'VD_mcg': 1.36,
        'VE': 0.43,
        'VB1': 0.214,
        'VB2': 3.113,
        'VB3': 14.888,
        'VB6': 1.224,
        'VB12': 67.01,
        'Magnesium': 20.34,
        'Choline': 376.6,
        'Folate': 327.70,
        'Pantothenic': 8.105,
    }
}

# 8. Spanish mackerel - SKIP (VD=292 IU/100g already verified)

# 9. Chicken skin (raw) - per 4.0 oz (113.0 g)
data['Chicken Skin'] = {
    'serving_g': 113.0,
    'serving_desc': '4.0 oz (113.0 g)',
    'raw': {
        'Calories': 394,
        'Protein': 15.06,
        'Fat': 36.556,
        'Phosphorus': 113.00,
        'Calcium': 12.43,
        'Iron': 1.22,
        'Zinc': 1.05,
        'Copper': 0.05,
        'Manganese': 0.021,
        'Potassium': 116.39,
        'Sodium': 71.19,
        'Selenium': 13.90,
        'VA_RAE_mcg': 85.88,
        'VD_mcg': 0.68,
        'VE': 0.00,
        'VB1': 0.037,
        'VB2': 0.078,
        'VB3': 4.505,
        'VB6': 0.102,
        'VB12': 0.26,
        'Magnesium': 14.69,
        'Choline': None,  # Not shown on page
        'Folate': 3.39,
        'Pantothenic': 0.782,
    }
}

# 10. Duck (meat only, raw) - per 1.0 unit yield from 1 lb (137.0 g)
data['Duck'] = {
    'serving_g': 137.0,
    'serving_desc': '1.0 unit yield from 1 lb (137.0 g)',
    'raw': {
        'Calories': 185,
        'Protein': 25.04,
        'Fat': 8.152,
        'Phosphorus': 278.11,
        'Calcium': 15.07,
        'Iron': 3.29,
        'Zinc': 2.60,
        'Copper': 0.35,
        'Manganese': 0.026,
        'Potassium': 371.27,
        'Sodium': 101.38,
        'Selenium': 19.04,
        'VA_RAE_mcg': 32.88,
        'VD_mcg': 0.14,
        'VE': 0.96,
        'VB1': 0.493,
        'VB2': 0.616,
        'VB3': 7.261,
        'VB6': 0.466,
        'VB12': 0.55,
        'Magnesium': 26.03,
        'Choline': 73.4,
        'Folate': 34.25,
        'Pantothenic': 2.192,
    }
}

# ============================================================
# CODE VALUES (current values in the recipe code)
# Order: chicken thigh, pork, chicken heart, beef heart, egg, chicken liver, beef liver, spanish mackerel, chicken skin, duck
# ============================================================

code_names = ['Chicken Thigh', 'Pork Loin', 'Chicken Heart', 'Beef Heart', 'Egg', 
              'Chicken Liver', 'Beef Liver', 'Spanish Mackerel', 'Chicken Skin', 'Duck']

code_values = {
    'Calories':    [119, 143, 153, 112, 143, 119, 135, 139, 349, 135],
    'Protein':     [19.6, 21.1, 15.6, 17.7, 12.6, 16.9, 20.4, 19.29, 13.3, 18.28],
    'Fat':         [4.3, 6.9, 9.3, 3.9, 9.9, 4.8, 3.6, 6.30, 32.4, 5.95],
    'Phosphorus':  [178, 197, 177, 212, 198, 297, 387, 171, 68, 203],
    'Calcium':     [9, 5, 12, 7, 56, 8, 5, 11, 11, 11],
    'Iron':        [0.8, 0.8, 5.9, 4.3, 1.8, 9.0, 4.9, 0.44, 0.7, 2.4],
    'Zinc':        [1.8, 1.9, 6.6, 2.4, 1.3, 2.7, 4.0, 0.51, 0.6, 1.9],
    'Copper':      [0.06, 0.06, 0.33, 0.39, 0.07, 0.49, 9.76, 0.046, 0.02, 0.24],
    'Manganese':   [0.02, 0.01, 0.05, 0.03, 0.03, 0.26, 0.31, 0.015, 0.01, 0.02],
    'Potassium':   [242, 389, 176, 287, 138, 230, 313, 446, 119, 271],
    'Sodium':      [95, 52, 74, 98, 142, 71, 69, 59, 51, 74],
    'Selenium':    [23.0, 32.5, 16.0, 21.8, 30.7, 54.6, 39.7, 36.5, 14.1, 14.0],
    'VA_IU':       [50, 7, 31, 0, 520, 11078, 16898, 98, 150, 24],
    'VD_IU':       [5, 12, 0, 0, 82, 12, 49, 16, 0, 0],
    'VE':          [0.2, 0.5, 0.7, 0.2, 1.1, 0.7, 0.5, 0.42, 0.3, 0.7],
    'VB1':         [0.07, 0.81, 0.13, 0.24, 0.04, 0.31, 0.19, 0.068, 0.01, 0.36],
    'VB2':         [0.16, 0.23, 0.73, 0.91, 0.46, 1.78, 2.76, 0.130, 0.07, 0.47],
    'VB3':         [5.3, 5.0, 4.8, 7.4, 0.1, 9.7, 13.2, 8.47, 2.5, 5.3],
    'VB6':         [0.33, 0.42, 0.29, 0.28, 0.14, 0.85, 1.08, 0.315, 0.05, 0.34],
    'VB12':        [0.4, 0.6, 7.3, 8.6, 0.9, 16.6, 59.3, 7.4, 0.3, 0.4],
    'Magnesium':   [23, 25, 15, 21, 12, 19, 20, 33, 10, 20],
    'Choline':     [65, 80, 65, 150, 293, 290, 333, 65, 46, 64],
    'Folate':      [6, 1, 72, 3, 47, 588, 290, 2, 1, 5],
    'Pantothenic': [1.01, 0.60, 2.51, 2.25, 1.53, 6.50, 7.17, 0.42, 0.53, 1.03],
}

# ============================================================
# CONVERT TO PER 100g AND COMPARE
# ============================================================

def convert_to_100g(raw_vals, serving_g):
    """Convert raw per-serving values to per 100g."""
    factor = 100.0 / serving_g
    result = {}
    for k, v in raw_vals.items():
        if v is None:
            result[k] = None
        else:
            result[k] = round(v * factor, 4)
    # Convert VA and VD to IU
    if result.get('VA_RAE_mcg') is not None:
        result['VA_IU'] = round(result['VA_RAE_mcg'] * 3.33, 1)
    else:
        result['VA_IU'] = None
    if result.get('VD_mcg') is not None:
        result['VD_IU'] = round(result['VD_mcg'] * 40, 1)
    else:
        result['VD_IU'] = None
    return result

# Nutrients to compare (matching code_values keys)
nutrients = ['Calories', 'Protein', 'Fat', 'Phosphorus', 'Calcium', 'Iron', 'Zinc',
             'Copper', 'Manganese', 'Potassium', 'Sodium', 'Selenium', 'VA_IU', 'VD_IU',
             'VE', 'VB1', 'VB2', 'VB3', 'VB6', 'VB12', 'Magnesium', 'Choline', 'Folate', 'Pantothenic']

# Items to verify (skip Spanish mackerel = index 7)
verify_items = ['Chicken Thigh', 'Pork Loin', 'Chicken Heart', 'Beef Heart', 'Egg',
                'Chicken Liver', 'Beef Liver', 'Chicken Skin', 'Duck']

# Map item name to code index
code_idx = {
    'Chicken Thigh': 0, 'Pork Loin': 1, 'Chicken Heart': 2, 'Beef Heart': 3,
    'Egg': 4, 'Chicken Liver': 5, 'Beef Liver': 6, 'Chicken Skin': 8, 'Duck': 9
}

print("=" * 120)
print("COMPREHENSIVE NUTRITIONAL DATA VERIFICATION - NutritionValue.org (USDA) vs Code Values")
print("=" * 120)

all_discrepancies = []

for item in verify_items:
    d = data[item]
    per100 = convert_to_100g(d['raw'], d['serving_g'])
    idx = code_idx[item]
    
    print(f"\n{'─' * 120}")
    print(f"  {item.upper()}")
    print(f"  Serving shown on site: {d['serving_desc']}")
    print(f"  Conversion factor: 100 / {d['serving_g']} = {100/d['serving_g']:.4f}")
    print(f"{'─' * 120}")
    print(f"  {'Nutrient':<16} {'Raw/Serving':>12} {'Per 100g (USDA)':>16} {'Code Value':>12} {'Diff %':>10} {'Status':>10}")
    print(f"  {'─'*16} {'─'*12} {'─'*16} {'─'*12} {'─'*10} {'─'*10}")
    
    for nut in nutrients:
        usda_val = per100.get(nut)
        code_val = code_values[nut][idx]
        
        # Get raw value for display
        if nut == 'VA_IU':
            raw_display = f"{d['raw'].get('VA_RAE_mcg', 'N/A')}"
            raw_label = f"{raw_display} mcg RAE"
        elif nut == 'VD_IU':
            raw_display = f"{d['raw'].get('VD_mcg', 'N/A')}"
            raw_label = f"{raw_display} mcg"
        else:
            raw_val = d['raw'].get(nut)
            raw_label = f"{raw_val}" if raw_val is not None else "N/A"
        
        if usda_val is None:
            usda_display = "N/A"
            diff_pct = "N/A"
            status = "NO DATA"
        else:
            usda_display = f"{usda_val:.2f}" if isinstance(usda_val, float) else str(usda_val)
            
            if code_val == 0 and usda_val == 0:
                diff_pct = "0.0%"
                status = "✓ OK"
            elif code_val == 0:
                diff_pct = "INF"
                status = "⚠ FLAG" if usda_val > 1 else "~ minor"
            elif usda_val == 0:
                diff_pct = "-100%"
                status = "⚠ FLAG" if code_val > 1 else "~ minor"
            else:
                pct = (usda_val - code_val) / code_val * 100
                diff_pct = f"{pct:+.1f}%"
                if abs(pct) > 15:
                    status = "⚠ FLAG"
                elif abs(pct) > 5:
                    status = "~ close"
                else:
                    status = "✓ OK"
        
        print(f"  {nut:<16} {raw_label:>12} {usda_display:>16} {code_val:>12} {diff_pct:>10} {status:>10}")
        
        if usda_val is not None and status == "⚠ FLAG":
            all_discrepancies.append((item, nut, usda_val, code_val, diff_pct))

# ============================================================
# SUMMARY OF DISCREPANCIES
# ============================================================

print(f"\n\n{'=' * 120}")
print("SUMMARY OF ALL DISCREPANCIES > 15%")
print(f"{'=' * 120}")
print(f"{'Item':<20} {'Nutrient':<16} {'USDA/100g':>12} {'Code Value':>12} {'Difference':>12}")
print(f"{'─'*20} {'─'*16} {'─'*12} {'─'*12} {'─'*12}")

for item, nut, usda_val, code_val, diff_pct in all_discrepancies:
    print(f"{item:<20} {nut:<16} {usda_val:>12.2f} {code_val:>12} {diff_pct:>12}")

print(f"\nTotal flagged discrepancies (>15%): {len(all_discrepancies)}")

# ============================================================
# CORRECTED VALUES TABLE (what the code SHOULD use)
# ============================================================

print(f"\n\n{'=' * 120}")
print("CORRECTED PER-100g VALUES (from USDA via NutritionValue.org)")
print("Order: chicken thigh, pork, chicken heart, beef heart, egg, chicken liver, beef liver, spanish mackerel, chicken skin, duck")
print(f"{'=' * 120}")

# Spanish mackerel values (kept as-is from code, except VD=292)
mackerel_code = {nut: code_values[nut][7] for nut in nutrients}
mackerel_code['VD_IU'] = 292  # Corrected value

for nut in nutrients:
    vals = []
    for item in ['Chicken Thigh', 'Pork Loin', 'Chicken Heart', 'Beef Heart', 'Egg',
                 'Chicken Liver', 'Beef Liver']:
        d = data[item]
        per100 = convert_to_100g(d['raw'], d['serving_g'])
        v = per100.get(nut)
        if v is not None:
            vals.append(f"{v:.2f}" if isinstance(v, float) and v < 100 else f"{v:.1f}")
        else:
            vals.append(f"{code_values[nut][code_idx[item]]}")  # keep code value if no USDA data
    
    # Spanish mackerel - use code values (already verified separately)
    vals.append(f"{mackerel_code[nut]}")
    
    for item in ['Chicken Skin', 'Duck']:
        d = data[item]
        per100 = convert_to_100g(d['raw'], d['serving_g'])
        v = per100.get(nut)
        if v is not None:
            vals.append(f"{v:.2f}" if isinstance(v, float) and v < 100 else f"{v:.1f}")
        else:
            vals.append(f"{code_values[nut][code_idx[item]]}")
    
    print(f"{nut:<16}: [{', '.join(vals)}]")
