import sys, os, json, time, wave
from faster_whisper import WhisperModel

shard, nshard = int(sys.argv[1]), int(sys.argv[2])
os.makedirs('out', exist_ok=True)

def dur(p):
    try:
        with wave.open(p) as w: return w.getnframes()/w.getframerate()
    except Exception: return 0

files = sorted(os.listdir('wav'))
files = [f for f in files if f.endswith('.wav')]
# longest-first within shard for better load balance
files.sort(key=lambda f: -dur('wav/'+f))
mine = [f for i, f in enumerate(files) if i % nshard == shard]

m = WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2", device="cpu",
                 compute_type="float32", cpu_threads=2)
t0 = time.time(); done = 0; tot = len(mine)
for f in mine:
    key = f[:-4]
    outp = f'out/{key}.json'
    if os.path.exists(outp): done += 1; continue
    try:
        segs, info = m.transcribe('wav/'+f, language="ja", beam_size=5, vad_filter=True,
                                  condition_on_previous_text=False, temperature=0.0,
                                  no_speech_threshold=0.6)
        rows = [{'s': round(s.start,1), 'e': round(s.end,1), 't': s.text.strip(),
                 'lp': round(s.avg_logprob,2), 'ns': round(s.no_speech_prob,2)} for s in segs]
        json.dump({'key': key, 'duration': round(info.duration,1), 'segments': rows},
                  open(outp,'w'), ensure_ascii=False)
    except Exception as e:
        json.dump({'key': key, 'error': str(e)[:200]}, open(outp,'w'), ensure_ascii=False)
    done += 1
    el = time.time()-t0
    print(f"[shard{shard}] {done}/{tot} {key} elapsed={el/60:.1f}m eta={(el/done*(tot-done))/60:.0f}m", flush=True)
print(f"[shard{shard}] DONE", flush=True)
