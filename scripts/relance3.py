#!/usr/bin/env python3
"""Relance des items tronqués, un par un, avec backoff sur 429."""
import json, pathlib, sys, time, urllib.error
sys.path.insert(0, "/root/work/benchmark-llm-fr/scripts")
from runner import call, HERE, PROMPTS

BASE = "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1"
KEYS = __import__("os").environ.get("BENCH_API_KEY", "")

# (slug, modèle, fichier source des troncatures)
TARGETS = {
    "qwen36_35b_a3b": "qwen3.6-35b-a3b",
    "qwen35_397b": "Qwen3.5-397B-A17B",
    "gemma_4_26b": "gemma-4-26b-a4b",
}

prompts = {json.loads(l)["id"]: json.loads(l) for l in PROMPTS.open(encoding="utf-8")}

def deja_ok(slug):
    """Items déjà obtenus proprement dans relance2."""
    p = HERE / f"runs/relance2_{slug}.jsonl"
    done = set()
    if p.exists():
        for line in p.open(encoding="utf-8"):
            r = json.loads(line)
            if not r.get("error"):
                done.add(r["id"])
    return done

for slug, model in TARGETS.items():
    src = HERE / f"runs/{slug}.jsonl"
    recs = [json.loads(l) for l in src.open(encoding="utf-8")]
    trunc = [r["id"] for r in recs if r.get("finish") == "length"]
    done = deja_ok(slug)
    todo = [i for i in trunc if i not in done]
    out = HERE / f"runs/relance3_{slug}.jsonl"
    print(f"== {slug}: {len(trunc)} tronqués, {len(done)} déjà repris, {len(todo)} à traiter", flush=True)
    with out.open("a", encoding="utf-8") as f:
        for pid in todo:
            p = prompts[pid]
            for attempt in range(6):
                t0 = time.time()
                try:
                    d = call(BASE, KEYS, model, p["prompt"], 16000, None, 0.8, timeout=600)
                    msg = d["choices"][0]["message"]
                    rec = {"id": pid, "family": p["family"], "model": model,
                           "content": msg.get("content") or "",
                           "reasoning": msg.get("reasoning") or msg.get("reasoning_content") or "",
                           "usage": d.get("usage", {}),
                           "finish": d["choices"][0].get("finish_reason"),
                           "latency_s": round(time.time() - t0, 2), "error": None}
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
                    print(f"  {pid} OK finish={rec['finish']} tok={rec['usage'].get('completion_tokens')}", flush=True)
                    break
                except urllib.error.HTTPError as e:
                    body = e.read().decode()[:160]
                    if e.code == 429:
                        wait = min(60, 5 * (attempt + 1))
                        print(f"  {pid} 429, attente {wait}s (essai {attempt+1}/6)", flush=True)
                        time.sleep(wait); continue
                    f.write(json.dumps({"id": pid, "family": p["family"], "model": model,
                                        "content": "", "error": f"HTTP {e.code}: {body}",
                                        "latency_s": round(time.time()-t0, 2)}, ensure_ascii=False) + "\n"); f.flush()
                    print(f"  {pid} HTTP {e.code}", flush=True); break
                except Exception as e:
                    print(f"  {pid} {type(e).__name__}: {e}", flush=True)
                    time.sleep(5); continue
            time.sleep(2)
    print(f"== {slug} terminé", flush=True)
print("terminé", flush=True)
