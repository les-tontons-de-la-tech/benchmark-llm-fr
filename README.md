# Benchmark LLM français — 120 tâches vérifiables

Banc d'évaluation en français pour modèles servis par API, avec **notation déterministe** :
aucun juge LLM. 120 tâches réparties en 6 familles, notées mécaniquement (regex, JSON parsé,
calcul exact, code réellement exécuté en sandbox).

Run publié : **17 modèles** servis par OVHcloud AI Endpoints, 23 novembre 2026.
Coût calculé sur les tokens réellement consommés, tarifs du **catalogue OVHcloud** (jamais ceux de
`/v1/models`, qui renvoie 0 pour onze modèles payants).

| Modèle | Note | Latence moy. | Tokens sortie | Coût / 120 tâches |
|---|---|---|---|---|
| gemma-4-26b-a4b | **98,3 %** (115/117) | 8,3 s | 1 127 | 5,61 c$ |
| Qwen3.5-397B-A17B | **98,3 %** (115/117) | 14,4 s | 2 313 | 118,38 c$ |
| Qwen3.6-27B | **98,3 %** (115/117) | 7,8 s | 1 108 | 42,72 c$ |
| gpt-oss-120b | 97,4 % (114/117) | 2,9 s | 212 | 1,31 c$ |
| Qwen3.8-27B | 97,4 % (114/117) | 6,0 s | 621 | 24,29 c$ |
| nemotron3-omni-30b | 96,6 % (113/117) | 2,5 s | 383 | 2,76 c$ |
| DeepSeek-V4.1-Flash-1017 | 95,7 % (112/117) | **1,6 s** | 302 | 4,80 c$ |
| nemotron3-nano-30b | 95,7 % (112/117) | 1,8 s | 329 | 0,95 c$ |
| Qwen2.5-VL-72B-Instruct | 95,7 % (112/117) | 2,0 s | 66 | 1,58 c$ |
| qwen3.6-35b-a3b | 95,7 % (112/117) | 14,0 s | 2 035 | 32,60 c$ |
| gpt-oss-20b | 94,9 % (111/117) | 2,3 s | 270 | **0,65 c$** |
| laguna-xs-2.1 | 94,9 % (111/117) | 5,4 s | 729 | 1,11 c$ |
| Meta-Llama-3_3-70B-Instruct | 94,9 % (111/117) | 2,8 s | 79 | 1,40 c$ |
| qwen3-vl-30b-a3b | 94,9 % (111/117) | **1,3 s** | 157 | 1,19 c$ |
| Olala-v1.0-mini-7A1B | 94,0 % (110/117) | 4,9 s | 1 458 | gratuit au catalogue |
| Mistral-Small-3.2-24B-Instruct-2506 | 92,3 % (108/117) | 4,4 s | 60 | 0,28 c$ |
| Qwen3.5-9B | 92,3 % (108/117) | 26,7 s | 2 886 | 6,31 c$ |

**Lecture honnête** : trois modèles à 98,3 % ne sont pas départageables — deux échecs d'écart sur
117 items. Ce qui tranche réellement, c'est le couple latence/coût : **gpt-oss-120b** tient 97,4 %
pour 1,31 c$ et 2,9 s, soit 90 fois moins cher que Qwen3.5-397B-A17B pour un point de moins.

**Le juge change le classement.** Sur les 109 seules tâches vérifiables mécaniquement,
`nemotron3-nano-30b` arrivait en tête à 99,1 % ; une fois les 8 items de rédaction libre jugés, il
tombe au 8e rang. C'est un petit modèle : la qualité du français le départage là où le code et
l'arithmétique ne le font pas. `gemma-4-26b-a4b`, lui, résiste et prend la tête.

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
| `francais` | accords, syntaxe, lexique | 10 déterministes + 8 jugés par Claude · 2 écartés |
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

Les items marqués `judge` sont notés par le juge LLM décrit ci-dessous ; un item non jugé est
compté comme non évalué, jamais comme un échec.

### Le juge des items de rédaction

8 items ne sont pas vérifiables mécaniquement (réécrire « malgré que », expliquer « censé/sensé »,
passer au style direct…). Ils sont jugés par **Claude Opus 5.5**, appelé via LiteLLM puis OpenRouter.

- **Hors compétition** : aucun modèle Anthropic n'est évalué dans ce banc, donc pas d'auto-préférence.
- **Température 0**, modèle épinglé, prompt de jugement fixé dans `scripts/juger.py`.
- **Réponse anonymisée** : le juge ne voit pas quel modèle a produit quoi.
- **Critères publiés d'avance** dans `judge_criteria.json` — le critère est écrit avant de voir les
  réponses, pas ajusté après.
- **Verdicts bruts publiés** dans `runs/jugement_claude.jsonl`, justification comprise : chacun peut
  contester un verdict item par item.

Un juge LLM reste un juge : c'est un arbitrage documenté, pas une vérité. Deux de ses verdicts
tranchés méritent le débat — `francais-12` exige que la règle de l'accord mentionne explicitement
le cas du sujet pour être validée, et `francais-19` sanctionne la coordination « est lent, vieux et
chauffe » (un adjectif et un verbe coordonnés). Les deux sont conformes au critère publié.

### Corrections appliquées avant publication

Quatre défauts de notation ont été trouvés en rejouant chaque checker sur une solution écrite à
la main — et corrigés avant de publier le moindre chiffre :

- `code-16` écarté : le test passait un `\n` littéral (item insoluble), puis l'énoncé lui-même
  s'est révélé ambigu (CSV 2×2) ;
- `code-14` : normalisation numérique (`2.00 Ko` = `2.0 Ko` = `2 Ko`), le format n'étant pas imposé ;
- `code-06` (FizzBuzz) : l'énoncé ne fixe pas le type des éléments ; un modèle qui renvoie `[1, 2,
  "Fizz"]` au lieu de `["1", "2", "Fizz"]` répond juste. Comparaison en texte quand l'attendu est
  une chaîne — trois modèles étaient pénalisés sur ce détail, ils remontent à 99,1 % ;
- `consignes-17` : guillemets ouvrants ignorés, ce n'est pas une violation de consigne ;
- `factuel-04` : 735 et 736 acceptés (1 ch métrique = 735,49875 W, troncature ou arrondi de 735,5) ;
- `francais-13` écarté : deux trous dans la phrase pour une réponse d'un seul mot ;
- cinq items de réécriture (`francais-04/08/10/19/20`) ont été testés en notation déterministe puis **remis au juge** : les listes d'acceptation produisaient des verdicts faux sur des réponses correctes (ex. « Il se trompe. », « Viens-tu ? »), et un faux positif sur une réponse hors sujet. Le test des checkers a tranché contre leur conversion.

## Structure

```
prompts.jsonl          # les 120 tâches + leur checker
scripts/build_prompts.py    # génère prompts.jsonl (graine 20261121)
scripts/runner.py           # interroge un modèle, reprise par id
scripts/relance.py          # rejoue des items au budget supérieur
scripts/check.py            # notation déterministe
scripts/report_compare.py   # tableaux comparatifs depuis runs/
judge_criteria.json         # critères de correction des 8 items jugés (publiés)
scripts/juger.py            # jugement par Claude via LiteLLM -> OpenRouter
runs/<modele>.jsonl         # réponses publiées du run du 23/11/2026
runs/jugement_claude.jsonl  # verdicts bruts du juge, justification incluse
RESULTATS.md                # rapport du run publié
RESULTATS-GENERE.md         # tableaux régénérés par report_compare.py
```

Les fichiers `runs/*.jsonl` contiennent les réponses réelles, raisonnement inclus : ils permettent
de **rejouer la notation sans rappeler l'API**, et de vérifier chaque score.

## Limites assumées

- Jeu orienté tâches courtes et vérifiables ; rien ici ne mesure le contexte long, le RAG, la
  rédaction longue, ni le coût d'un usage réel en production.
- Les 8 items de rédaction libre sont jugés par un LLM unique (Claude Opus 5.5). Un juge n'est pas
  une vérité : ses verdicts sont publiés bruts dans `runs/jugement_claude.jsonl` pour être contestés.
  2 items de français restent écartés.
- Échantillon de 109 items notés : un écart de 2 à 3 points n'est pas significatif (intervalle de
  confiance à 95 % d'environ ± 2,5 points autour de 98 %, ± 4 à 5 points autour de 90 %). Les quatre
  premiers du classement ont le même score à un item près : **ne pas y lire une hiérarchie**.
- Trois modèles raisonneurs ont des items restés tronqués après relance au budget maximal de
  16 000 tokens (`qwen3.6-35b-a3b` 3, `Qwen3.5-397B-A17B` 1, `Qwen3.5-9B` 1) : c'est un
  comportement réel du modèle sur ces items, pas un défaut de mesure, mais cela compte en échec.
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
