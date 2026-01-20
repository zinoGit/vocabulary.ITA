#!/usr/bin/env python3
import sys, re, unicodedata, requests

url = "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/it_IT/it_IT.dic"
resp = requests.get(url)
resp.raise_for_status()
lines = resp.text.splitlines()

words = set()
vowel_re = re.compile(r"[AEIOUaeiouÀÈÉÌÍÒÓÙÚàèéìíòóùú]")

for i, line in enumerate(lines):
    if i == 0:
        continue
    if not line:
        continue
    if line.startswith('/'):  
        continue
    # split on '/' to expand alternates; this may also split flags but we'll filter later
    parts = line.split('/')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # skip tokens containing apostrophe
        if "'" in part:
            continue
        # require at least one vowel (helps filter flag tokens)
        if not vowel_re.search(part):
            continue
        # normalize and remove diacritics
        s = unicodedata.normalize('NFKD', part)
        s = ''.join(ch for ch in s if not unicodedata.combining(ch))
        # keep only ASCII letters
        s = re.sub(r'[^A-Za-z]', '', s)
        s = s.lower()
        # exclude short tokens (<=3)
        if len(s) <= 3:
            continue
        words.add(s)

out = '\n'.join(sorted(words))
with open('it_wordlist.txt', 'w', encoding='utf-8') as f:
    f.write(out)
print(f"Wrote {len(words)} words to it_wordlist.txt")