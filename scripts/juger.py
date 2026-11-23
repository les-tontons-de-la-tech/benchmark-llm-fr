#!/usr/bin/env python3
"""Jugement des 8 items de rédaction par Claude (via LiteLLM -> OpenRouter).

Protocole : réponse anonymisée, critère publié (judge_criteria.json), température 0,
modèle épinglé, sortie JSON stricte. Verdicts bruts écrits tels quels.
"""
import json, os, pathlib, sys, time, urllib.request

HERE = pathlib.Path("/root/work/benchmark-llm-fr")
RUNS = HERE / "runs"
OUT = RUNS / "jugement_claude.jsonl"
MODELE = "claude-juge"          # litellm -> openrouter/anthropic/claude-opus-5.5
LITELLM = "http://127.0.0.1:4000/v1/chat/completions"


def env(path, key):
    for line in open(path, encoding="utf-8"):
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


KEY = env("/root/.hermes/.env", "LITELLM_MASTER_KEY")
if not KEY:
    sys.exit("master key LiteLLM introuvable")

prompts = {json.loads(l)["id"]: json.loads(l) for l in (HERE / "prompts.jsonl").open(encoding="utf-8")}
criteria = json.loads((HERE / "judge_criteria.json").read_text(encoding="utf-8"))
IDS = list(criteria)

SYS = ("Tu es un correcteur de français rigoureux. On te donne une consigne, un critère de "
       "correction, et la réponse d'un candidat anonyme. Tu appliques strictement le critère. "
       "Tu ne récompenses pas la longueur, tu ne sanctionnes pas le style. "
       "Tu réponds UNIQUEMENT par un objet JSON valide de la forme "
       '{"verdict": "OK" ou "KO", "justification": "une phrase"} et rien de plus.')

# réponses par modèle
reponses = {}
for f in sorted(RUNS.glob("*.jsonl")):
    if f.name.startswith("jugement"):
        continue
    for line in f.open(encoding="utf-8"):
        r = json.loads(line)
        if r["id"] in criteria and not r.get("error"):
            m = r["model"]
            prev = reponses.get((m, r["id"]))
            # garder la réponse la plus complète (relances incluses)
            if prev is None or len(r.get("content") or "") > len(prev):
                reponses[(m, r["id"])] = r.get("content") or ""

modeles = sorted({m for (m, _) in reponses})
print(f"{len(modeles)} modèles x {len(IDS)} items = {len(modeles)*len(IDS)} jugements", flush=True)

done = set()
if OUT.exists():
    for line in OUT.open(encoding="utf-8"):
        try:
            r = json.loads(line)
            if r.get("verdict"):
                done.add((r["modele"], r["id"]))
        except Exception:
            pass

with OUT.open("a", encoding="utf-8") as f:
    for m in modeles:
        for pid in IDS:
            rep = reponses.get((m, pid))
            if rep is None or (m, pid) in done:
                continue
            user = (f"CONSIGNE DONNÉE AU CANDIDAT :\n{prompts[pid]['prompt']}\n\n"
                    f"CRITÈRE DE CORRECTION :\n{criteria[pid]}\n\n"
                    f"RÉPONSE DU CANDIDAT :\n<<<{rep[:4000]}>>>")
            body = {"model": MODELE, "temperature": 0, "max_tokens": 400,
                    "messages": [{"role": "system", "content": SYS},
                                 {"role": "user", "content": user}]}
            rec = {"modele": m, "id": pid, "modele_juge": MODELE}
            for attempt in range(4):
                try:
                    req = urllib.request.Request(LITELLM, data=json.dumps(body).encode(),
                        headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY})
                    with urllib.request.urlopen(req, timeout=180) as r:
                        d = json.load(r)
                    txt = d["choices"][0]["message"]["content"].strip()
                    rec["brut"] = txt
                    rec["usage"] = d.get("usage", {})
                    s, e = txt.find("{"), txt.rfind("}")
                    obj = json.loads(txt[s:e+1]) if s >= 0 else {}
                    rec["verdict"] = (obj.get("verdict") or "").upper()[:2]
                    rec["justification"] = obj.get("justification", "")
                    break
                except Exception as ex:
                    rec["erreur"] = f"{type(ex).__name__}: {str(ex)[:200]}"
                    time.sleep(3 * (attempt + 1))
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            print(f"  {m:32s} {pid:12s} {rec.get('verdict','?')}", flush=True)
            time.sleep(0.3)
print("terminé", flush=True)
