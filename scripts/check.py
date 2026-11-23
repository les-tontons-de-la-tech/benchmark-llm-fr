#!/usr/bin/env python3
"""Notation déterministe des réponses du benchmark Olala.

Aucun juge LLM : format, JSON, calculs, code exécuté, réponses factuelles sont
vérifiés mécaniquement. Seules les familles "francais" (et 2 items factuels à
réponse ouverte) restent à noter à la main / au juge.

Sortie : scores.json + un résumé lisible.
"""
import json, pathlib, re, subprocess, sys, tempfile, textwrap, unicodedata

HERE = pathlib.Path(__file__).resolve().parent.parent
RUNS = HERE / "runs"

def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("\u00a0", " ").replace("’", "'").replace("«", '"').replace("»", '"')
    return re.sub(r"\s+", " ", s).strip().lower()

def strip_fences(t):
    t = t or ""
    m = re.search(r"```(?:python|json)?\s*(.+?)```", t, re.S)
    return m.group(1).strip() if m else t.strip()

def extract_number(t):
    if not t: return None
    t = norm(t).replace(" ", "")
    m = re.findall(r"reponse:\s*(-?[\d ]+(?:[.,]\d+)?)", t)
    if m:
        v = m[-1].replace(" ", "").replace(",", ".")
        try: return float(v)
        except Exception: pass
    nums = re.findall(r"-?\d+(?:[.,]\d+)?", t)
    if not nums: return None
    try: return float(nums[-1].replace(",", "."))
    except Exception: return None

def check_python(code, spec):
    code = strip_fences(code)
    if not code: return False, "aucun code"
    harness = ["import json,sys"]
    harness.append(textwrap.dedent(code))
    harness.append("\nTESTS=" + repr(spec["tests"]))
    _NORM = """
import re as _re
def _norm(v):
    if isinstance(v, str):
        v = _re.sub(r"(\\d)\\.0+(?![0-9])", r"\\1", v.strip())
        v = _re.sub(r"\\s+", " ", v)
    elif isinstance(v, list):
        v = [_norm(x) for x in v]
    return v
"""
    harness.append(_NORM)
    harness.append(f"""
out=[]
for args,expected in TESTS:
    try:
        got=globals()[{spec['fn']!r}](*args)
        if isinstance(got,set): got=sorted(got)
        out.append(_norm(got)==_norm(expected))
    except Exception as e:
        out.append(False)
print(json.dumps(out))
""")
    src = "\n".join(harness)
    try:
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, "-I", "-c", src], capture_output=True,
                               text=True, timeout=10, cwd=d)
        if p.returncode != 0:
            return False, f"exécution: {p.stderr.strip()[:120]}"
        res = json.loads(p.stdout.strip().splitlines()[-1])
        return all(res), f"{sum(res)}/{len(res)} tests"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

def check(content, reasoning, ck):
    if isinstance(ck, str) or ck.get("type") == "judge":
        return None, "à noter (juge)"
    if ck.get("type") == "skip":
        return None, ck.get("why", "écarté")
    t = ck["type"]; txt = content or ""
    if t == "final_number":
        v = extract_number(txt)
        return (v is not None and abs(v - ck["expect"]) < 0.51), f"attendu {ck['expect']}, lu {v}"
    if t == "final_number_list":
        v = extract_number(txt)
        ok = v is not None and any(abs(v - a) < 0.51 for a in ck["accept"])
        return ok, f"attendu {ck['accept']}, lu {v}"
    if t == "int":
        m = re.search(r"-?\d+", norm(txt)); v = int(m.group()) if m else None
        return v == ck["expect"], f"attendu {ck['expect']}, lu {v}"
    if t == "json_fields":
        raw = strip_fences(txt)
        m = re.search(r"\{.*\}", raw, re.S)
        try:
            got = json.loads(m.group()) if m else json.loads(raw)
        except Exception as e:
            return False, f"JSON invalide: {type(e).__name__}"
        ok = True
        for k, exp in ck["expect"].items():
            gv = got.get(k)
            if isinstance(exp, int):
                try: gv = int(str(gv).replace(" ", "").replace("€", "").replace("\u00a0", ""))
                except Exception: ok = False; continue
            elif isinstance(exp, str):
                ok = ok and (norm(exp) in norm(str(gv)))
                continue
            ok = ok and (gv is None or gv == exp or norm(str(gv)) == norm(str(exp)))
        return ok, f"champs {list(got)[:6]}"
    if t == "exact_norm":
        clean = lambda x: re.sub(r"\s*([\-<>=;,])\s*", r"\1", norm(x)).strip(' ."')
        return clean(txt) == clean(ck["expect"]), f"lu: {clean(txt)[:60]}"
    if t == "contains_all":
        nt = norm(txt)
        ok = all(any(norm(a) in nt for a in group) for group in ck["any"])
        return ok, f"manquants: {[g for g in ck['any'] if not any(norm(a) in nt for a in g)]}"
    if t == "set_sep":
        got = {norm(x) for x in re.split(r"[;]", txt) if x.strip()}
        exp = {norm(x) for x in ck["expect"]}
        return got == exp, f"lu: {sorted(got)[:5]}"
    if t == "one_of":
        return norm(txt).strip(' .') in [norm(x) for x in ck["accept"]], f"lu: {norm(txt)[:40]}"
    if t == "uppercase":
        return norm(txt.replace(".", "").strip()) == norm(ck["expect"]) and txt.strip().isupper(), f"lu: {txt[:40]}"
    if t == "wordcount":
        return len(norm(txt).split()) == ck["n"], f"{len(norm(txt).split())} mots"
    if t == "bullet_lines":
        lines = [l for l in txt.strip().splitlines() if l.strip()]
        return len(lines) == ck["n"] and all(l.strip().startswith(("-", "•")) for l in lines), f"{len(lines)} lignes"
    if t == "sentence":
        n = len(re.findall(r"[.!?]", txt.strip()))
        words = len(norm(txt).split())
        has = all(norm(w) in norm(txt) for w in ck["must"])
        return (n <= 1 and words <= ck["max_words"] and has), f"{words} mots, mots-clés {has}"
    if t == "constraint":
        sents = [s for s in re.split(r"[.!?]", txt.strip()) if s.strip()]
        starts_il = norm(txt).strip().startswith("il ")
        return (len(sents) <= ck["max_sentences"] and not starts_il), f"{len(sents)} phrases, commence par il: {starts_il}"
    if t == "count_sep":
        parts = [p for p in txt.strip().split(ck["sep"]) if p.strip()]
        return len(parts) == ck["n"], f"{len(parts)} éléments"
    if t == "starts_wordcount":
        head = re.sub(r'^[\s"«”\'\u201c\u201d]+', "", norm(txt))
        return head.startswith(ck["start"]) and len(norm(txt).split()) == ck["n"], f"{len(norm(txt).split())} mots"
    if t == "starts":
        # guillemets ouvrants et espaces initiaux ignorés : ponctuation typographique, pas une violation
        head = re.sub(r'^[\s"«”\'\u201c\u201d]+', "", norm(txt))
        return head.startswith(norm(ck["start"])), f"lu: {norm(txt)[:40]}"
    if t == "max_words":
        w = len(norm(txt).split())
        hit = (ck.get("expect_contains", "") in norm(txt)) if ck.get("expect_contains") else any(norm(a) in norm(txt) for a in ck.get("any_of", [""]))
        return (w <= ck["n"] and hit), f"{w} mots"
    if t == "regex":
        return bool(re.match(ck["pattern"], txt.strip())), f"lu: {txt.strip()[:40]}"
    if t == "json_list":
        raw = strip_fences(txt); m = re.search(r"\{.*\}", raw, re.S)
        try: got = json.loads(m.group() if m else raw)
        except Exception: return False, "JSON invalide"
        return got.get(ck["key"]) == ck["expect"], f"lu: {str(got.get(ck['key']))[:40]}"
    if t == "python":
        return check_python(txt, ck["expect"])
    return None, f"checker inconnu {t}"

def main():
    prompts = {json.loads(l)["id"]: json.loads(l) for l in (HERE / "prompts.jsonl").open(encoding="utf-8")}
    report = {}
    for f in sorted(RUNS.glob("*.jsonl")):
        recs = [json.loads(l) for l in f.open(encoding="utf-8")]
        if not recs: continue
        model = recs[0]["model"]
        per_fam, details = {}, []
        for r in recs:
            ck = prompts[r["id"]]["checker"]
            ok, why = check(r.get("content", ""), r.get("reasoning", ""), ck)
            if r.get("error"): ok, why = False, f"erreur: {r['error'][:80]}"
            details.append({"id": r["id"], "family": r["family"], "ok": ok, "why": why})
            per_fam.setdefault(r["family"], {"ok": 0, "total": 0, "n/a": 0})
            if ok is None: per_fam[r["family"]]["n/a"] += 1
            else:
                per_fam[r["family"]]["total"] += 1
                per_fam[r["family"]]["ok"] += int(bool(ok))
        scored = {k: v for k, v in per_fam.items() if v["total"]}
        tot_ok = sum(v["ok"] for v in scored.values()); tot = sum(v["total"] for v in scored.values())
        report[model] = {"file": f.name, "n": len(recs), "global": round(100*tot_ok/tot, 1) if tot else None,
                         "passed": tot_ok, "scored_items": tot,
                         "families": {k: {"score": round(100*v["ok"]/v["total"], 1), **v} for k, v in scored.items()},
                         "details": details}
    out = HERE / "scores.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    for m, r in report.items():
        print(f"\n== {m} : {r['global']}% ({r['passed']}/{r['scored_items']} items notés, {r['n']} réponses)")
        for k, v in r["families"].items():
            print(f"   {k:12s} {v['score']:5.1f}%  {v['ok']}/{v['total']}" + (f"  (+{v['n/a']} à juger)" if v["n/a"] else ""))
    print(f"\nDétail -> {out}")

if __name__ == "__main__":
    main()
