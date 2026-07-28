import json, os, subprocess, concurrent.futures as cf
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
os.makedirs('wav', exist_ok=True); os.makedirs('mp4', exist_ok=True)
items = json.load(open('all_items.json'))
tasks, seen = [], set()
for it in items:
    code = it.get('code')
    if code in seen: continue
    seen.add(code)
    if it.get('media_type') == 2 and it.get('video_versions'):
        tasks.append((code, it['video_versions'][0]['url'], it.get('taken_at'), it.get('video_duration') or 0))
    elif it.get('media_type') == 8:
        for j, ch in enumerate(it.get('carousel_media') or []):
            if ch.get('media_type') == 2 and ch.get('video_versions'):
                tasks.append((f"{code}__{j+1}", ch['video_versions'][0]['url'], it.get('taken_at'), ch.get('video_duration') or 0))
json.dump([{'key':t[0],'taken_at':t[2],'dur':t[3]} for t in tasks], open('clips.json','w'))
print("tasks:", len(tasks), flush=True)

def work(t):
    key, url, _, _ = t
    wav = f'wav/{key}.wav'
    if os.path.exists(wav) and os.path.getsize(wav) > 1000: return key, 'skip'
    mp4 = f'mp4/{key}.mp4'
    r = subprocess.run(['curl','-sS','--cacert','/root/.ccr/ca-bundle.crt','--max-time','300','-o',mp4,url], capture_output=True, text=True)
    if not os.path.exists(mp4) or os.path.getsize(mp4) < 10000: return key, 'DL_FAIL'
    r = subprocess.run([FF,'-y','-loglevel','error','-i',mp4,'-vn','-ar','16000','-ac','1',wav], capture_output=True, text=True)
    os.remove(mp4)
    return key, ('ok' if os.path.exists(wav) else 'FF_FAIL:'+r.stderr[:80])

done = 0
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    for key, st in ex.map(work, tasks):
        done += 1
        if st != 'ok' and st != 'skip': print(f"[{done}] {key} {st}", flush=True)
        elif done % 25 == 0: print(f"[{done}/{len(tasks)}] ok", flush=True)
print("EXTRACT DONE", flush=True)
