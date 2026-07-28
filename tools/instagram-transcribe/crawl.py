import json, subprocess, time, sys, os

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('IG_USER')
if not USER:
    sys.exit('usage: crawl.py <instagram_username>  (or set IG_USER)')
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
def get(url):
    for attempt in range(5):
        r = subprocess.run(['curl','-sS','--cacert','/root/.ccr/ca-bundle.crt','-A',UA,
            '-H','x-ig-app-id: 936619743392459','-H',f'Referer: https://www.instagram.com/{USER}/', url],
            capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            if d.get('status') == 'fail':
                time.sleep(5*(attempt+1)); continue
            return d
        except Exception:
            time.sleep(5*(attempt+1))
    return None

base = f"https://www.instagram.com/api/v1/feed/user/{USER}/username/?count=33"
items, url, page = [], base, 0
while True:
    d = get(url)
    if not d: print("FAILED at page", page); break
    items += d['items']; page += 1
    print(f"page {page}: +{d['num_results']} total={len(items)} more={d.get('more_available')}", flush=True)
    if not d.get('more_available') or not d.get('next_max_id'): break
    url = base + "&max_id=" + d['next_max_id']
    time.sleep(2)
json.dump(items, open('all_items.json','w'))
print("TOTAL ITEMS:", len(items))
