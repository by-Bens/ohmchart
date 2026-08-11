import re
import os

PUBLIC_DIR = "public"

all_pages = {}
for root, _, files in os.walk(PUBLIC_DIR):
    for f in files:
        if f == "index.html":
            url = root[len(PUBLIC_DIR):].replace("\\", "/") + "/"
            all_pages[url.replace("//", "/")] = os.path.join(root, f)

hrefs = {}
for url, path in all_pages.items():
    html = open(path, encoding="utf-8").read()
    for m in re.finditer(r'href=["\']?(/[^"\'\s>]*)', html):
        h = m.group(1).split("#")[0]
        if h and not h.startswith(("//", "/css", "/js")):
            hrefs.setdefault(h, []).append(url)

broken = {}
for h, sources in hrefs.items():
    check = h if h.endswith("/") else h + "/"
    if check not in all_pages:
        broken[h] = sources

print(f"Pages built: {len(all_pages)}")
print(f"Links checked: {len(hrefs)}")
print(f"Broken links: {len(broken)}")
for h, sources in broken.items():
    print(f"  BROKEN: {h}  (linked from {sources[0]})")