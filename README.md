# Benchmark LLM français — 120 tâches vérifiables

Banc d'évaluation en français pour modèles servis par API, avec **notation déterministe** :
aucun juge LLM. 120 tâches réparties en 6 familles, notées mécaniquement (regex, JSON parsé,
calcul exact, code réellement exécuté en sandbox).

Premier run publié : comparatif **Olala mini 7A1B / Mistral-Small 3.2 24B / Qwen3.5-9B**
via OVHcloud AI Endpoints, le 23 novembre 2026.

| Modèle | Note | Latence moy. | Tokens sortie | Coût / 120 tâches |
|---|---|---|---|---|
| Olala-v1.0-mini-7A1B | **98,1 %** (103/105) | 4,9 s | 1 458 | gratuit au catalogue |
| Mistral-Small-3.2-24B-Instruct-2506 | **93,3 %** (98/105) | 4,4 s | 60 | 0,28 c$ |
| Qwen3.5-9B | **90,5 %** (95/105) | 26,7 s | 2 886 | 6,31 c$ |

Détail, échecs item par item et analyse : [RESULTATS.md](RESULTATS.md).

## Ce que ce benchmark est, et ce qu'il n'est pas

**C'est** un test sur mesure, conçu pour des tâches courtes et **vérifiables mécaniquement** :
respect de consignes strictes, extraction JSON, arithmétique, code exécuté, français vérifiable,
faits chiffrés. Il mesure ce qu'un modèle d'API doit réussir pour être branché dans un pipeline
éditorial ou métier, pas sa culture générale.

**Ce n'est pas** un benchmark académique. Aucune question n'est reprise de MMLU, GSM8K,
HumanEval ou d'un autre jeu public. Les scores **ne sont donc pas comparables** à ceux publiés
par les éditeurs de modèles, ni à ceux d'un leaderboard.

## Les 6 familles (20 tâches chacune)

| Famille | Ce qu'elle vérifie | Notation |
|---|---|---|
| `consignes` | format imposé (longueur en mots, casse, JSON strict, séparateurs) | regex, comptage, parse |
| `extraction` | extraire 4 champs d'un texte métier | JSON parsé, champs comparés |
| `maths` | arithmétique sur des valeurs tirées (graine fixe) | nombre final exact |
| `code` | 20 fonctions Python | **code exécuté** en sandbox (`-I`, timeout 10 s) sur des tests unitaires |
| `francais` | accords, syntaxe, lexique | 8 vérifiables · 10 à juger · 2 écartés |
| `factuel` | constantes et dates du domaine technique | nombre/année final |

## Reproduire

Prérequis : Python 3.10+, une clé **OVHcloud AI Endpoints** (projet Public Cloud avec moyen de
paiement). Le service est compatible OpenAI.

```bash
export BENCH_API_KEY='votre-clé'

# 1. générer le jeu de test (déterministe, graine fixe)
python3 scripts/build_prompts.py

# 2. interroger un modèle — reprise automatique sur les id déjà présents
python3 scripts/runner.py \
  --model Mistral-Small-3.2-24B-Instruct-2506 \
  --base-url https://oai.endpoints.kepler.ai.cloud.ovh.net/v1 \
  --max-tokens 8000 --temperature 0.8 \
  --out runs/mon-run.jsonl

# 3. noter et produire le rapport
python3 scripts/report_compare.py
```

`runner.py` accepte `--only <famille>`, `--limit N`, `--exclude-from <fichier>` (pour paralléliser
un modèle lent par famille) et `--effort` (transmis en `reasoning_effort`). `relance.py` rejoue des
items précis avec un budget de tokens plus large.

### Régler le problème du raisonnement

Les modèles qui raisonnent (Qwen3.5-9B) consomment énormément de tokens sur des questions
triviales. Pour un budget donné, toujours **relancer les items tronqués** (`finish_reason: length`)
avec un budget supérieur avant de les compter en échec — sinon le score est faussé à la baisse.
Sur OVHcloud AI Endpoints, `max_tokens` plafonne à **16 384**.

## Notation

`checker` dans `prompts.jsonl` décrit la vérification de chaque item. Types disponibles :
`one_of`, `exact_norm`, `wordcount`, `bullet_lines`, `json_fields`, `json_list`, `final_number`,
`final_number_list`, `int`, `contains_all`, `set_sep`, `uppercase`, `sentence`, `constraint`,
`starts`, `starts_wordcount`, `regex`, `python`, et `skip` pour les items écartés (énoncé ambigu).

Les items marqués `judge` ne sont **pas** notés automatiquement : ils sont exclus du score, et
comptés à part.

### Corrections appliquées avant publication

Quatre défauts de notation ont été trouvés en rejouant chaque checker sur une solution écrite à
la main — et corrigés avant de publier le moindre chiffre :

- `code-16` écarté : le test passait un `\n` littéral (item insoluble), puis l'énoncé lui-même
  s'est révélé ambigu (CSV 2×2) ;
- `code-14` : normalisation numérique (`2.00 Ko` = `2.0 Ko` = `2 Ko`), le format n'étant pas imposé ;
- `consignes-17` : guillemets ouvrants ignorés, ce n'est pas une violation de consigne ;
- `factuel-04` : 735 et 736 acceptés (1 ch métrique = 735,49875 W, troncature ou arrondi de 735,5) ;
- `francais-13` écarté : deux trous dans la phrase pour une réponse d'un seul mot.

## Structure

```
prompts.jsonl          # les 120 tâches + leur checker
scripts/build_prompts.py    # génère prompts.jsonl (graine 20261121)
scripts/runner.py           # interroge un modèle, reprise par id
scripts/relance.py          # rejoue des items au budget supérieur
scripts/check.py            # notation déterministe
scripts/report_compare.py   # tableaux comparatifs depuis runs/
runs/<modele>.jsonl         # réponses publiées du run du 23/11/2026
RESULTATS.md                # rapport du run publié
RESULTATS-GENERE.md         # tableaux régénérés par report_compare.py
```

Les fichiers `runs/*.jsonl` contiennent les réponses réelles, raisonnement inclus : ils permettent
de **rejouer la notation sans rappeler l'API**, et de vérifier chaque score.

## Limites assumées

- Jeu orienté tâches courtes et vérifiables ; rien ici ne mesure le contexte long, le RAG, la
  rédaction longue, ni le coût d'un usage réel en production.
- 10 items de français restent à juger et 2 ont été écartés : le score « français » ne porte que sur 8.
- Échantillon de 105 items notés : un écart de 2 à 3 points n'est pas significatif.
- La latence mesurée est le temps total de l'appel HTTP, raisonnement inclus, pas le temps avant
  premier token.
- Le jeu est calibré sur un domaine (hardware, cloud, français technique) et n'a pas été validé
  par des tiers.

## Licence

- **Code** (`scripts/`) : MIT — voir [LICENSE](LICENSE).
- **Jeu de données et réponses** (`prompts.jsonl`, `runs/`, `RESULTATS*.md`) : CC BY 4.0,
  réutilisation libre avec attribution.

Réutilisez-le, contestez-le, ajoutez vos modèles. Si vous corrigez un checker, ouvrez une issue :
c'est comme ça que les chiffres valent quelque chose.

---

**Les Tontons de la Tech** — https://lestontons.tech
