#!/usr/bin/env python3
"""Rapport comparatif multi-modèles à partir de runs/*.jsonl + prompts.jsonl.

Usage : python3 report_compare.py
Sortie : rapport-comparatif.md + tableau console.
"""
import json, pathlib, statistics, sys
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "scripts"))
from check import check  # notation déterministe partagée
RUNS = HERE / "runs"

# Tarifs USD / token, relevés sur https://catalog.endpoints.ai.ovh.net/rest/v1/models_v2
# le 23/11/2026 (champs price_usd + price_unit). NE JAMAIS déduire un prix de /v1/models :
# cet endpoint renvoie 0 pour 11 modèles payants. Source : prices_catalog.json.
PRICING = {
    "Olala-v1.0-mini-7A1B": (0.0, 0.0),
    "Mistral-Small-3.2-24B-Instruct-2506": (0.0000001, 0.00000031),
    "Qwen3.5-9B": (0.00000012, 0.00000018),
    "Qwen3.6-27B": (0.00000047, 0.00000319),
    "Qwen3.8-27B": (0.00000047, 0.00000319),
    "gpt-oss-20b": (0.00000005, 0.00000018),
    "gpt-oss-120b": (0.00000009, 0.00000047),
    "DeepSeek-V4.1-Flash-1017": (0.00000031, 0.00000125),
    "gemma-4-26b-a4b": (0.0000001, 0.00000041),
    "laguna-xs-2.1": (0.00000006, 0.00000012),
    "Meta-Llama-3_3-70B-Instruct": (0.00000074, 0.00000074),
    "nemotron3-nano-30b": (0.00000006, 0.00000023),
    "nemotron3-omni-30b": (0.00000019, 0.00000057),
    "Qwen2.5-VL-72B-Instruct": (0.00000101, 0.00000101),
    "Qwen3.5-397B-A17B": (0.00000071, 0.00000425),
    "qwen3-vl-30b-a3b": (0.00000015, 0.00000058),
    "qwen3.6-35b-a3b": (0.0000002, 0.00000133),
}

prompts = {}
for line in (HERE / "prompts.jsonl").open(encoding="utf-8"):
    p = json.loads(line)
    prompts[p["id"]] = p


def load(path):
    return [json.loads(l) for l in path.open(encoding="utf-8") if l.strip()]


def score(recs):
    fam = defaultdict(lambda: {"ok": 0, "total": 0, "na": 0})
    details = {}
    for r in recs:
        ck = prompts[r["id"]]["checker"]
        ok, why = check(r.get("content", ""), r.get("reasoning", ""), ck)
        if r.get("error"):
            ok, why = False, f"erreur: {r['error'][:80]}"
        details[r["id"]] = {"ok": ok, "why": why}
        f = fam[r["family"]]
        if ok is None:
            f["na"] += 1
        else:
            f["total"] += 1
            f["ok"] += int(bool(ok))
    scored = {k: v for k, v in fam.items() if v["total"]}
    ok = sum(v["ok"] for v in scored.values())
    return {"global": round(100 * ok / sum(v["total"] for v in scored.values()), 1) if ok or scored else None,
            "passed": ok, "n": sum(v["total"] for v in scored.values()),
            "families": scored, "details": details}


models = {}
for f in sorted(RUNS.glob("*.jsonl")):
    if f.name.startswith("_test") or f.stat().st_size == 0:
        continue
    recs = load(f)
    if not recs:
        continue
    m = recs[0]["model"]
    if m in models:  # plusieurs fichiers pour un même modèle : fusion par id,
        # un enregistrement en erreur ne doit jamais écraser un enregistrement valide
        merged = {r["id"]: r for r in models[m]["recs"]}
        for r in recs:
            old = merged.get(r["id"])
            if old is not None and r.get("error") and not old.get("error"):
                continue
            merged[r["id"]] = r
        recs = list(merged.values())
    lat = [r.get("latency_s", 0) for r in recs if not r.get("error")]
    toks = [r.get("usage", {}).get("completion_tokens", 0) for r in recs if not r.get("error")]
    tok_in = [r.get("usage", {}).get("prompt_tokens", 0) for r in recs if not r.get("error")]
    trunc = sum(1 for r in recs if r.get("finish") == "length")
    errs = sum(1 for r in recs if r.get("error"))
    s = score(recs)
    pr = PRICING.get(m)
    if pr is None:
        cost = None          # tarif inconnu : on affichera "n.d.", jamais "gratuit"
    else:
        pin, pout = pr
        cost = sum(tok_in) * pin + sum(toks) * pout
    models[m] = {"recs": recs, "score": s, "lat": lat, "toks": toks,
                 "trunc": trunc, "errs": errs, "cost": cost, "n": len(recs)}

order = sorted(models, key=lambda m: -(models[m]["score"]["global"] or 0))
fams = sorted({f for m in models for f in models[m]["score"]["families"]})

out = ["# Comparatif modèles — 120 tâches françaises (OVHcloud AI Endpoints)", "",
       "_Notation déterministe (regex, JSON, code exécuté, calcul exact). Aucun juge LLM._", "",
       "## Synthèse", "",
       "| Modèle | Note vérifiable | Items | Latence moy. | Tokens sortie | Tronqués | Erreurs | Coût /120 tâches |",
       "|---|---|---|---|---|---|---|---|"]
for m in order:
    d = models[m]
    sc = d["score"]
    if d["cost"] is None:
        cost = "n.d."          # tarif absent du catalogue : ne jamais écrire « gratuit »
    elif d["cost"] == 0:
        cost = "gratuit"
    else:
        cost = f"{d['cost']*100:.2f} c$"
    out.append(f"| {m} | **{sc['global']} %** | {sc['passed']}/{sc['n']} | "
               f"{statistics.mean(d['lat']):.1f} s | {statistics.mean(d['toks']):.0f} | "
               f"{d['trunc']} | {d['errs']} | {cost} |")

out += ["", "## Par famille", "",
        "| Famille | " + " | ".join(order) + " |",
        "|---|" + "---|" * len(order)]
for fam in fams:
    row = []
    for m in order:
        v = models[m]["score"]["families"].get(fam)
        row.append(f"{v['score'] if False else round(100*v['ok']/v['total'],1)} % ({v['ok']}/{v['total']})" if v else "—")
    out.append(f"| {fam} | " + " | ".join(row) + " |")

# items discriminants
out += ["", "## Items discriminants", ""]
for fam in fams:
    ids = [i for i, p in prompts.items() if p["family"] == fam]
    diff = [i for i in ids if len({bool(models[m]["score"]["details"].get(i, {}).get("ok")) for m in order}) > 1]
    if diff:
        out.append(f"**{fam}** — " + ", ".join(sorted(diff)))
out.append("")

# échecs communs
common = [i for i in prompts if all(models[m]["score"]["details"].get(i, {}).get("ok") is False for m in order)]
out += ["## Échecs communs à tous les modèles (à inspecter : checker trop strict ?)", ""]
for i in sorted(common):
    why = models[order[0]]["score"]["details"][i]["why"]
    out.append(f"- `{i}` — {why}")
out.append("")

# échecs par modèle
for m in order:
    fails = [i for i, v in models[m]["score"]["details"].items() if v["ok"] is False]
    out += [f"## Échecs — {m} ({len(fails)})", ""]
    for i in sorted(fails):
        c = next((r.get("content") or "" for r in models[m]["recs"] if r["id"] == i), "")
        out.append(f"- `{i}` — {models[m]['score']['details'][i]['why']} — `{c[:110].strip()}`")
    out.append("")

# --- reproductibilité -------------------------------------------------------
import hashlib
h = hashlib.sha256((HERE / "prompts.jsonl").read_bytes()).hexdigest()
out += [
    "## Paramètres et reproductibilité", "",
    f"- Jeu de test : 120 tâches, 6 familles, hash SHA-256 `{h}` (v1.1 ; v1 corrigée, voir plus bas).",
    "- Température 0,8 · top_p 0,9 · budget de sortie 8 000 tokens, porté à 16 000 (Olala, limite API) "
    "et 24 000 (Qwen) pour les items tronqués, relancés une fois.",
    "- Olala : `reasoning_effort=high` (réglage recommandé par OVHcloud). Mistral et Qwen : réglage par défaut, "
    "sans paramètre de raisonnement — Qwen3.5-9B raisonne de lui-même (`reasoning_tokens` dans l'usage).",
    "- Endpoint : `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1`, clé AI Endpoints authentifiée "
    "(400 req/min/projet/modèle).",
    "- Latence = temps total de l'appel HTTP (inclut le raisonnement), pas le temps avant premier token.",
    "",
    "### Corrections de notation appliquées avant publication", "",
    "- `code-14` : normalisation numérique des sorties (`2.00 Ko` = `2.0 Ko` = `2 Ko`) — l'énoncé ne fixe pas le format.",
    "- `code-16` : écarté — CSV 2×2 à deux lectures défendables (paires ligne à ligne vs en-tête + une ligne).",
    "- `consignes-17` : guillemets ouvrants ignorés (« Non, … » vaut « Non, … »).",
    "- `factuel-04` : 735 et 736 acceptés (1 ch = 735,49875 W : troncature ou arrondi de 735,5).",
    "- Trois items tronqués ont été relancés avec un budget supérieur avant d'être comptés en échec ; "
    "`factuel-19` (Qwen) part en boucle même à 24 000 tokens.",
    "",
]
(HERE / "RESULTATS-GENERE.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out[:40]))
print(f"\n-> {HERE/'rapport-comparatif.md'}")
