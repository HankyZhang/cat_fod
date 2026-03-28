# -*- coding: utf-8 -*-
import io
import re
import sys
import urllib.parse
import urllib.request
from html import unescape

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE = 'https://www.nutritionvalue.org'

FOODS = {
    '鸡腿肉': {
        'query': 'chicken thigh raw',
        'include': ['thigh', 'raw'],
        'exclude': ['cooked', 'fried', 'roasted', 'skin'],
    },
    '猪瘦肉': {
        'query': 'pork loin raw',
        'include': ['pork', 'loin', 'raw'],
        'exclude': ['cooked', 'roasted', 'fried'],
    },
    '鸡心': {
        'query': 'chicken heart raw',
        'include': ['chicken', 'heart', 'raw'],
        'exclude': ['cooked', 'simmered'],
    },
    '牛心': {
        'query': 'beef heart raw',
        'include': ['beef', 'heart', 'raw'],
        'exclude': ['cooked', 'braised'],
    },
    '鸡蛋': {
        'query': 'egg whole raw fresh',
        'include': ['egg', 'whole', 'raw'],
        'exclude': ['cooked', 'fried', 'scrambled'],
    },
    '鸡肝': {
        'query': 'chicken liver raw',
        'include': ['chicken', 'liver', 'raw'],
        'exclude': ['cooked', 'simmered', 'fried'],
    },
    '牛肝': {
        'query': 'beef liver raw',
        'include': ['beef', 'liver', 'raw'],
        'exclude': ['cooked', 'fried', 'braised'],
    },
    '鱼': {
        'query': 'mackerel raw',
        'include': ['mackerel', 'raw'],
        'exclude': ['cooked', 'smoked'],
    },
    '鸡皮': {
        'query': 'chicken skin raw thighs',
        'include': ['chicken', 'skin', 'raw'],
        'exclude': ['cooked', 'fried'],
    },
}

CURRENT = {
    '鸡腿肉': {'能量':119,'蛋白质':19.6,'脂肪':4.3,'磷':178,'钙':9,'铁':0.8,'锌':1.8,'铜':0.06,'锰':0.02,'硒':23.0,'VA':50,'VD':5,'VE':0.2,'VB1':0.07,'VB2':0.16,'VB3':5.3,'VB6':0.33,'VB12':0.4},
    '猪瘦肉': {'能量':143,'蛋白质':21.1,'脂肪':6.9,'磷':197,'钙':5,'铁':0.8,'锌':1.9,'铜':0.06,'锰':0.01,'硒':32.5,'VA':7,'VD':12,'VE':0.5,'VB1':0.81,'VB2':0.23,'VB3':5.0,'VB6':0.42,'VB12':0.6},
    '鸡心': {'能量':153,'蛋白质':15.6,'脂肪':9.3,'磷':177,'钙':12,'铁':5.9,'锌':6.6,'铜':0.33,'锰':0.05,'硒':16.0,'VA':31,'VD':0,'VE':0.7,'VB1':0.13,'VB2':0.73,'VB3':4.8,'VB6':0.29,'VB12':7.3},
    '牛心': {'能量':112,'蛋白质':17.7,'脂肪':3.9,'磷':212,'钙':7,'铁':4.3,'锌':2.4,'铜':0.39,'锰':0.03,'硒':21.8,'VA':0,'VD':0,'VE':0.2,'VB1':0.24,'VB2':0.91,'VB3':7.4,'VB6':0.28,'VB12':8.6},
    '鸡蛋': {'能量':143,'蛋白质':12.6,'脂肪':9.9,'磷':198,'钙':56,'铁':1.8,'锌':1.3,'铜':0.07,'锰':0.03,'硒':30.7,'VA':520,'VD':82,'VE':1.1,'VB1':0.04,'VB2':0.46,'VB3':0.1,'VB6':0.14,'VB12':0.9},
    '鸡肝': {'能量':119,'蛋白质':16.9,'脂肪':4.8,'磷':297,'钙':8,'铁':9.0,'锌':2.7,'铜':0.49,'锰':0.26,'硒':54.6,'VA':11078,'VD':12,'VE':0.7,'VB1':0.31,'VB2':1.78,'VB3':9.7,'VB6':0.85,'VB12':16.6},
    '牛肝': {'能量':135,'蛋白质':20.4,'脂肪':3.6,'磷':387,'钙':5,'铁':4.9,'锌':4.0,'铜':9.76,'锰':0.31,'硒':39.7,'VA':16898,'VD':49,'VE':0.5,'VB1':0.19,'VB2':2.76,'VB3':13.2,'VB6':1.08,'VB12':59.3},
    '鱼': {'能量':205,'蛋白质':18.6,'脂肪':13.9,'磷':217,'钙':12,'铁':1.6,'锌':0.6,'铜':0.07,'锰':0.01,'硒':44.1,'VA':167,'VD':360,'VE':1.5,'VB1':0.18,'VB2':0.31,'VB3':9.1,'VB6':0.40,'VB12':8.7},
    '鸡皮': {'能量':349,'蛋白质':13.3,'脂肪':32.4,'磷':68,'钙':11,'铁':0.7,'锌':0.6,'铜':0.02,'锰':0.01,'硒':14.1,'VA':150,'VD':0,'VE':0.3,'VB1':0.01,'VB2':0.07,'VB3':2.5,'VB6':0.05,'VB12':0.3},
}

NUTRIENT_PATTERNS = {
    '能量': [('Calories', 'kcal')],
    '蛋白质': [('Protein', 'g')],
    '脂肪': [('Fat', 'g')],
    '钙': [('Calcium', 'mg')],
    '铁': [('Iron', 'mg')],
    '锌': [('Zinc', 'mg')],
    '铜': [('Copper', 'mg')],
    '锰': [('Manganese', 'mg')],
    '磷': [('Phosphorus', 'mg')],
    '钾': [('Potassium', 'mg')],
    '钠': [('Sodium', 'mg')],
    '硒': [('Selenium', 'mcg')],
    'VA': [('Vitamin A, RAE', 'mcg'), ('Retinol', 'mcg')],
    'VD': [('Vitamin D', 'mcg'), ('Vitamin D (D2 + D3)', 'mcg')],
    'VE': [('Vitamin E (alpha-tocopherol)', 'mg')],
    'VB1': [('Thiamin', 'mg')],
    'VB2': [('Riboflavin', 'mg')],
    'VB3': [('Niacin', 'mg')],
    'VB6': [('Vitamin B6', 'mg')],
    'VB12': [('Vitamin B12', 'mcg')],
    '亚油酸': [('Octadecadienoic acid', 'g')],
}

TAG_RE = re.compile(r'<[^>]+>')


def clean_text(text: str) -> str:
    text = TAG_RE.sub('', text)
    text = unescape(text)
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def search_link(query: str, include: list[str], exclude: list[str]) -> str | None:
    html = get(BASE + '/search.php?food_query=' + urllib.parse.quote_plus(query))
    links = re.findall(r'href=[\'\"]([^\'\"]*nutritional_value\.html)[\'\"]', html)
    seen = []
    for href in links:
        if href not in seen:
            seen.append(href)
    for href in seen:
        low = urllib.parse.unquote(href).lower()
        if all(term in low for term in include) and not any(term in low for term in exclude):
            return href if href.startswith('http') else BASE + href
    if not seen:
        return None
    href = seen[0]
    return href if href.startswith('http') else BASE + href


def extract_serving_grams(html: str) -> float | None:
    m = re.search(r'contains\s+[\d\.]+\s+calories\s+per\s+([\d\.]+)\s+g\s+serving', html, re.I)
    if m:
        return float(m.group(1))
    m = re.search(r'unit=1\.0[^=]*=\s*([\d\.]+)\s*g', html)
    if m:
        return float(m.group(1))
    return None


def extract_rows(html: str) -> dict[str, tuple[float, str]]:
    rows: dict[str, tuple[float, str]] = {}
    for left, value, unit in re.findall(r"<tr><td class='left'>(.*?)</td><td class='right'>([\d\.]+)&nbsp;([a-zA-Z]+)</td>", html, re.S | re.I):
        key = clean_text(left)
        if key.startswith('\xa0') or key.startswith('&nbsp;'):
            continue
        rows[key] = (float(value), unit)
    return rows


def extract_value(html: str, rows: dict[str, tuple[float, str]], nutrient: str) -> tuple[float | None, str | None]:
    if nutrient == '能量':
        m = re.search(r"id='calories'>([\d\.]+)<", html)
        if m:
            return float(m.group(1)), 'kcal'
    for key, unit in NUTRIENT_PATTERNS[nutrient]:
        if key in rows:
            return rows[key]
    return None, None


def convert_per_100g(value: float, serving_g: float, unit: str, nutrient: str) -> float:
    per100 = value / serving_g * 100
    if nutrient == 'VA':
        # NutritionValue typically exposes Vitamin A as mcg RAE; current table uses IU.
        # For retinol-dominant animal foods, 1 mcg RAE ≈ 3.33 IU.
        if unit == 'mcg':
            return per100 * 3.33
    if nutrient == 'VD':
        # Vitamin D shown as mcg; convert to IU with 1 mcg = 40 IU.
        if unit == 'mcg':
            return per100 * 40
    return per100


for label, cfg in FOODS.items():
    print('\n' + '='*60)
    print(label)
    link = search_link(cfg['query'], cfg['include'], cfg['exclude'])
    print('LINK', link)
    if not link:
        print('NO LINK FOUND')
        continue
    html = get(link)
    serving = extract_serving_grams(html)
    parsed_rows = extract_rows(html)
    print('SERVING_G', serving)
    if not serving:
        print('NO SERVING SIZE')
        continue
    rows = {}
    for nutrient in NUTRIENT_PATTERNS:
        value, unit = extract_value(html, parsed_rows, nutrient)
        if value is not None:
            rows[nutrient] = round(convert_per_100g(value, serving, unit, nutrient), 3)
    print('EXTRACTED', rows)
    if label in CURRENT:
        comp = []
        for k, v in CURRENT[label].items():
            if k in rows:
                new = rows[k]
                diff = abs(new - v) / max(abs(v), 1e-9) * 100
                comp.append((k, v, new, diff))
        comp.sort(key=lambda x: x[3], reverse=True)
        print('TOP_DIFFS', comp[:8])
    if '亚油酸' in rows:
        print('LINOLEIC_PER_100G', rows['亚油酸'])
