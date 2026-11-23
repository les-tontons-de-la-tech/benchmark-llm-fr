#!/usr/bin/env python3
"""Rattrapage des jugements sans verdict : parsing tolérant, retry sur contenu vide."""
import json, pathlib, re, time, urllib.request

HERE = pathlib.Path("/root/work/benchmark-llm-fr")
OUT = HERE / "runs/jugement_claude.jsonl"
MAP = "/root/.hermes/.env"


def envkey(path, key):
    for line in open(path, encoding="utf-8"):
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


KEY = envkey(MAP, "LITELLM_MASTER_KEY")
prompts = {json.loads(l)["id"]: json.loads(l) for l in (HERE / "prompts.jsonl").open(encoding="utf-8")}
criteria = json.loads((HERE / "judge_criteria.json").read_text(encoding="utf-8"))

# réponses par modèle
reponses = {}
for f in sorted((HERE / "runs").glob("*.jsonl")):
    if f.name.startswith("jugement"):
        continue
    for line in f.open(encoding="utf-8"):
        r = json.loads(line)
        if r["id"] in criteria and not r.get("error"):
            k = (r["model"], r["id"])
            if k not in reponses or len(r.get("content") or "") > len(reponses[k]):
                reponses[k] = r.get("content") or ""

recs = [json.loads(l) for l in OUT.open(encoding="utf-8")]
bad = [(x["modele"], x["id"]) for x in recs if not x.get("verdict")]
print(f"{len(bad)} jugements à rattraper", flush=True)

SYS = ("Tu es un correcteur de français rigoureux. Tu appliques strictement le critère fourni. "
       'Réponds UNIQUEMENT par un objet JSON : {"verdict": "OK" ou "KO", "justification": "une phrase"}.')

f = OUT.open("a", encoding="utf-8")
for modele, pid in bad:
    rep = reponses.get((modele, pid), "")
    user = (f"CONSIGNE :\n{prompts[pid]['prompt']}\n\nCRITÈRE :\n{criteria[pid]}\n\n"
            f"RÉPONSE DU CANDIDAT :\n<<<{rep[:4000]}>>>")
    body = {"model": "claude-juge", "temperature": 0, "max_tokens": 600,
            "messages": [{"role": "system", "content": SYS}, {"role": "user", "content": user}]}
    verdict = just = brut = None
    for attempt in range(6):
        try:
            req = urllib.request.Request("http://127.0.0.1:4000/v1/chat/completions",
                data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            msg = d["choices"][0]["message"]
            txt = (msg.get("content") or msg.get("reasoning") or "").strip()
            if not txt:
                time.sleep(4); continue
            brut = txt
            m = re.search(r'"verdict"\s*:\s*"(OK|KO)"', txt, re.I)
            j = re.search(r'"justification"\s*:\s*"((?:[^"\\]|\\.)*)"', txt)
            if m:
                verdict = m.group(1).upper()
                just = (j.group(1) if j else "")[:400]
                break
        except Exception as ex:
            time.sleep(3 * (attempt + 1))
    f.write(json.dumps({"modele": modele, "id": pid, "modele_juge": "claude-juge",
                        "brut": brut, "verdict": verdict, "justification": just or "",
                        "rattrapage": True}, ensure_ascii=False) + "\n")
    f.flush()
    print(f"  {modele:32s} {pid:12s} {verdict}", flush=True)
    time.sleep(0.3)
f.close()
print("rattrapage terminé", flush=True)
