#!/usr/bin/env python3
"""Runner du benchmark Olala : API compatible OpenAI (OVH AI Endpoints / OpenRouter).

Usage :
  python3 runner.py --model Olala-v1.0-mini-7A1B --base-url https://oai.endpoints.kepler.ai.cloud.ovh.net/v1 \
                    --out runs/olala.jsonl --limit 3
Reprise : les prompts déjà présents dans --out sont sautés.
"""
import argparse, json, os, pathlib, time, urllib.request, urllib.error

HERE = pathlib.Path(__file__).resolve().parent.parent
PROMPTS = HERE / "prompts.jsonl"

def load_prompts(limit=None, only=None):
    ps = [json.loads(l) for l in PROMPTS.open(encoding="utf-8")]
    if only:
        fams = set(only.split(","))
        ps = [p for p in ps if p["family"] in fams]
    return ps[:limit] if limit else ps

def done_ids(path):
    if not path.exists(): return set()
    out = set()
    for l in path.open(encoding="utf-8"):
        try: out.add(json.loads(l)["id"])
        except Exception: pass
    return out

def call(base, key, model, prompt, max_tokens, effort=None, temperature=0.2, timeout=180):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens, "temperature": temperature, "top_p": 0.9}
    if effort:
        body["reasoning_effort"] = effort  # AI Endpoints refuse chat_template_kwargs
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(), headers={
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {key}"} if key else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--api-key", default=os.environ.get("BENCH_API_KEY", ""))
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="")
    ap.add_argument("--max-tokens", type=int, default=1600)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--effort", default="")
    ap.add_argument("--sleep", type=float, default=0.0, help="pause entre deux appels (s)")
    ap.add_argument("--retries", type=int, default=4)
    ap.add_argument("--exclude-from", default="", help="fichier(s) jsonl dont les ids sont déjà traités (séparés par des virgules)")
    a = ap.parse_args()

    out = HERE / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    seen = done_ids(out)
    for extra in [x for x in a.exclude_from.split(",") if x.strip()]:
        seen |= done_ids(HERE / extra.strip())
    prompts = [p for p in load_prompts(a.limit, a.only) if p["id"] not in seen]
    print(f"{a.model}: {len(prompts)} prompts à traiter", flush=True)

    with out.open("a", encoding="utf-8") as f:
        for i, p in enumerate(prompts, 1):
            t0 = time.time()
            rec = {"id": p["id"], "family": p["family"], "model": a.model, "prompt": p["prompt"]}
            for attempt in range(a.retries + 1):
                try:
                    d = call(a.base_url, a.api_key, a.model, p["prompt"], a.max_tokens,
                             a.effort or None, a.temperature)
                    msg = d["choices"][0]["message"]
                    rec.update({"content": msg.get("content") or "",
                                "reasoning": msg.get("reasoning") or msg.get("reasoning_content") or "",
                                "usage": d.get("usage", {}),
                                "finish": d["choices"][0].get("finish_reason"),
                                "latency_s": round(time.time() - t0, 2), "error": None})
                    break
                except urllib.error.HTTPError as e:
                    txt = e.read().decode()[:300]
                    rec.update({"content": "", "error": f"HTTP {e.code}: {txt}",
                                "latency_s": round(time.time() - t0, 2)})
                    if e.code in (429, 500, 502, 503, 504) and attempt < a.retries:
                        try: wait = int(float(e.headers.get("retry-after") or 0)) + 2
                        except Exception: wait = 0
                        if not (5 <= wait <= 120): wait = min(20 * (attempt + 1), 120)
                        wait = max(wait, 5)
                        print(f"  {p['id']} HTTP {e.code} -> pause {wait}s", flush=True)
                        time.sleep(wait); continue
                    break
                except Exception as e:
                    rec.update({"content": "", "error": f"{type(e).__name__}: {e}",
                                "latency_s": round(time.time() - t0, 2)})
                    if attempt < a.retries:
                        time.sleep(10); continue
                    break
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            tag = "OK " if not rec.get("error") else "ERR"
            print(f"[{i}/{len(prompts)}] {tag} {p['id']} {rec.get('latency_s')}s", flush=True)
            if a.sleep: time.sleep(a.sleep)
    print("terminé:", out)

if __name__ == "__main__":
    main()
