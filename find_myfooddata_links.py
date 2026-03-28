# -*- coding: utf-8 -*-
import re
import sys
import io
import urllib.parse
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

queries = [
    ('鸡腿肉', 'site:tools.myfooddata.com chicken thigh boneless skinless raw'),
    ('猪瘦肉', 'site:tools.myfooddata.com pork loin raw'),
    ('鸡心', 'site:tools.myfooddata.com chicken heart raw'),
    ('牛心', 'site:tools.myfooddata.com beef heart raw'),
    ('鸡蛋', 'site:tools.myfooddata.com egg whole raw'),
    ('鸡肝', 'site:tools.myfooddata.com chicken liver raw'),
    ('牛肝', 'site:tools.myfooddata.com beef liver raw'),
    ('鱼', 'site:tools.myfooddata.com mackerel raw'),
    ('鸡皮', 'site:tools.myfooddata.com chicken skin raw'),
]

headers = {
    'User-Agent': 'Mozilla/5.0'
}

for label, query in queries:
    url = 'https://duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        m = re.search(r'uddg=(https%3A%2F%2Ftools\.myfooddata\.com%2Fnutrition%2Dfacts%2F[^"&]+)', html)
        if m:
            print(label, urllib.parse.unquote(m.group(1)))
        else:
            print(label, 'NO_LINK')
    except Exception as e:
        print(label, 'ERROR', repr(e))
