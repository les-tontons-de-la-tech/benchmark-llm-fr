#!/usr/bin/env python3
"""Relance ciblée d'items (tronqués faute de budget) avec un budget plus large.

python3 relance.py --model M --ids id1,id2 --out runs/relance.jsonl [--max-tokens 24000] [--effort high]
"""
import argparse, json, pathlib, time, urllib.error
from runner import call, HERE, PROMPTS

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--ids", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--max-tokens", type=int, default=24000)
ap.add_argument("--effort", default="")
ap.add_argument("--temperature", type=float, default=0.8)
ap.add_argument("--timeout", type=int, default=180)
ap.add_argument("--base-url", default="https://oai.endpoints.kepler.ai.cloud.ovh.net/v1")
ap.add_argument("--api-key", default=__import__("os").environ.get("BENCH_API_KEY", ""))
a = ap.parse_args()

prompts = {json.loads(l)["id"]: json.loads(l) for l in PROMPTS.open(encoding="utf-8")}
ids = [i for i in a.ids.split(",") if i.strip()]
out = HERE / a.out
out.parent.mkdir(parents=True, exist_ok=True)
print(f"{a.model}: relance de {len(ids)} items, budget {a.max_tokens}", flush=True)

with out.open("a", encoding="utf-8") as f:
    for pid in ids:
        p = prompts[pid]
        t0 = time.time()
        rec = {"id": pid, "family": p["family"], "model": a.model, "prompt": p["prompt"]}
        try:
            d = call(a.base_url, a.api_key, a.model, p["prompt"], a.max_tokens,
                     a.effort or None, a.temperature, timeout=a.timeout)
            msg = d["choices"][0]["message"]
            rec.update({"content": msg.get("content") or "",
                        "reasoning": msg.get("reasoning") or msg.get("reasoning_content") or "",
                        "usage": d.get("usage", {}),
                        "finish": d["choices"][0].get("finish_reason"),
                        "latency_s": round(time.time() - t0, 2), "error": None})
        except urllib.error.HTTPError as e:
            rec.update({"content": "", "error": f"HTTP {e.code}: {e.read().decode()[:200]}",
                        "latency_s": round(time.time() - t0, 2)})
        except Exception as e:
            rec.update({"content": "", "error": f"{type(e).__name__}: {e}",
                        "latency_s": round(time.time() - t0, 2)})
        f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
        print(f"  {pid} finish={rec.get('finish')} tok={rec.get('usage',{}).get('completion_tokens')} "
              f"{rec.get('latency_s')}s", flush=True)
print("ok")
