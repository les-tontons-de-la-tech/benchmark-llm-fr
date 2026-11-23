# Comparatif modèles — 120 tâches françaises (OVHcloud AI Endpoints)

_Banc maison écrit le 21 novembre 2026 (120 questions rédigées pour ce test, aucune reprise d'un benchmark public), notation déterministe — regex, JSON, code exécuté, calcul exact — sans juge LLM. Ce n'est pas un benchmark académique et les scores ne sont pas comparables à ceux publiés par les éditeurs._

## À retenir

- **Olala mini 7A1B gagne sur les tâches vérifiables** (98,1 %), en particulier là où la consigne est contraignante : 20/20 sur le respect de format, contre 14/20 pour Mistral. C'est le seul des trois à obéir systématiquement (« réponds uniquement par… », « exactement 12 mots », « termines par RÉPONSE: »).
- **Mistral-Small 3.2 24B est le plus factuel** (18/18 sur les faits vérifiables) mais le plus bavard : il enrobe ses réponses d'introductions et de guillemets, ce qui lui coûte 6 items sur 20 en consignes. Il reste le plus économe en tokens (60 en moyenne).
- **Qwen3.5-9B est le plus lent et le plus cher** : il raisonne de lui-même pour des questions triviales (2 886 tokens de sortie en moyenne, jusqu'à 24 000 et 225 s sur un seul item, avec une boucle de raisonnement qui ne converge jamais). Son score est le plus bas des trois, pour un coût 22 fois supérieur à Mistral.
- **Sur ce jeu, le petit modèle français gratuit d'OVHcloud n'est pas un compromis** : il est premier en qualité vérifiable, rapide (4,9 s) et sans coût au catalogue. Ses deux seuls échecs sont factuels et réels : il date la fondation d'OVHcloud de 2005 (1999) et le Power Delivery 3.1 de 100 W (240 W).
- **Ce que le test ne dit pas** : les 11 items de rédaction libre en français et 2 items factuels ouverts ne sont pas notés (aucun juge LLM) ; le jeu est orienté réponses courtes et vérifiables. Rien ici ne mesure la tenue sur contexte long, le RAG ou la rédaction longue.

## Synthèse

| Modèle | Note vérifiable | Items | Latence moy. | Tokens sortie | Tronqués | Erreurs | Coût /120 tâches |
|---|---|---|---|---|---|---|---|
| Olala-v1.0-mini-7A1B | **98.1 %** | 103/105 | 4.9 s | 1458 | 0 | 0 | gratuit |
| Mistral-Small-3.2-24B-Instruct-2506 | **93.3 %** | 98/105 | 4.4 s | 60 | 0 | 0 | 0.28 c$ |
| Qwen3.5-9B | **90.5 %** | 95/105 | 26.7 s | 2886 | 1 | 0 | 6.31 c$ |

## Par famille

| Famille | Olala-v1.0-mini-7A1B | Mistral-Small-3.2-24B-Instruct-2506 | Qwen3.5-9B |
|---|---|---|---|
| code | 100.0 % (19/19) | 94.7 % (18/19) | 84.2 % (16/19) |
| consignes | 100.0 % (20/20) | 70.0 % (14/20) | 95.0 % (19/20) |
| extraction | 100.0 % (20/20) | 100.0 % (20/20) | 85.0 % (17/20) |
| factuel | 88.9 % (16/18) | 100.0 % (18/18) | 83.3 % (15/18) |
| francais | 100.0 % (8/8) | 100.0 % (8/8) | 100.0 % (8/8) |
| maths | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) |

## Items discriminants

**code** — code-06, code-14, code-18
**consignes** — consignes-03, consignes-09, consignes-13, consignes-14, consignes-19, consignes-20
**extraction** — extraction-03, extraction-06, extraction-08
**factuel** — factuel-08, factuel-11, factuel-17, factuel-19, factuel-20

## Échecs communs à tous les modèles (à inspecter : checker trop strict ?)


## Échecs — Olala-v1.0-mini-7A1B (2)

- `factuel-08` — attendu 1999, lu 2005.0 — `RÉPONSE: 2005`
- `factuel-11` — attendu 240, lu 100.0 — `Le port USB‑C Power Delivery en mode PD 3.1 maximal délivre jusqu’à 100 watts. RÉPONSE: 100`

## Échecs — Mistral-Small-3.2-24B-Instruct-2506 (7)

- `code-18` — 0/1 tests — ````python
def devise(n):
    return f"{n:,.2f} €"
````
- `consignes-03` — 8 mots — `Cœur électronique reliant tous les composants informatiques essentiels`
- `consignes-09` — lu: voici les noms listes par ordre alphabetique : balzac,hugo,z — `Voici les noms listés par ordre alphabétique :

Balzac, Hugo, Zola`
- `consignes-13` — 6 mots — `"Aujourd'hui, je profite du soleil printemier."`
- `consignes-14` — lu: LE PROTOCOLE SERT À RÉSOUDRE LES NOMS DE — `LE PROTOCOLE SERT À RÉSOUDRE LES NOMS DE DOMAINE EST LE DNS`
- `consignes-19` — lu: Voici la chaîne demandée :

```
OK-2026  — `Voici la chaîne demandée :

```
OK-2026 42
```

(La somme de 40 et 2 est 42.)`
- `consignes-20` — lu: pour classer les temperatures de la plus froide a la plus ch — `Pour classer les températures de la plus froide à la plus chaude, nous comparons les valeurs numériques :

- *`

## Échecs — Qwen3.5-9B (10)

- `code-06` — 0/1 tests — ````python
def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:`
- `code-14` — 0/2 tests — ````python
def convertir_octets(n):
    if n < 1024:
        return n, "B"
    elif n < 1024 ** 2:
        re`
- `code-18` — 0/1 tests — ````python
def devise(n):
    return f"{n:,.2f}".replace(',', ' ').replace('.', ',') + " €"
````
- `consignes-14` — lu: 

LE PROTOCOLE DNS — `LE PROTOCOLE DNS`
- `extraction-03` — champs ['modele', 'site', 'prix_ht', 'garantie_mois'] — `{"modele": "Switch Cisco Catalyst 9300", "site": null, "prix_ht": 6480, "garantie_mois": 12}`
- `extraction-06` — champs ['modele', 'site', 'prix_ht', 'garantie_mois'] — `{
  "modele": "HP Z4 G5",
  "site": null,
  "prix_ht": 4300,
  "garantie_mois": 36
}`
- `extraction-08` — champs ['modele', 'site', 'prix_ht', 'garantie_mois'] — `{
  "modele": "cluster GPU de Grenoble",
  "site": "",
  "prix_ht": 412000,
  "garantie_mois": 12
}`
- `factuel-17` — attendu 1996, lu 1998.0 — `Le premier standard USB (USB 1.0) a été publié en 1998.
RÉPONSE: 1998`
- `factuel-19` — attendu [299792, 300000], lu None — ``
- `factuel-20` — attendu [24, 28], lu 20.0 — `Les processeurs grand public de la série Ryzen 7000 (AM5) exposent un total de **20** voies PCIe (PCIe lanes`

## Paramètres et reproductibilité

- Jeu de test : 120 tâches, 6 familles, hash SHA-256 `06f56e5895e7303b5b5d99325509a172a492549e0d6a52b11aff772c94dd8eca` (v1.1 ; v1 corrigée, voir plus bas).
- Température 0,8 · top_p 0,9 · budget de sortie 8 000 tokens, porté à 16 000 (Olala, limite API) et 24 000 (Qwen) pour les items tronqués, relancés une fois.
- Olala : `reasoning_effort=high` (réglage recommandé par OVHcloud). Mistral et Qwen : réglage par défaut, sans paramètre de raisonnement — Qwen3.5-9B raisonne de lui-même (`reasoning_tokens` dans l'usage).
- Endpoint : `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1`, clé AI Endpoints authentifiée (400 req/min/projet/modèle).
- Latence = temps total de l'appel HTTP (inclut le raisonnement), pas le temps avant premier token.

### Corrections de notation appliquées avant publication

- `code-14` : normalisation numérique des sorties (`2.00 Ko` = `2.0 Ko` = `2 Ko`) — l'énoncé ne fixe pas le format.
- `code-16` : écarté — CSV 2×2 à deux lectures défendables (paires ligne à ligne vs en-tête + une ligne).
- `consignes-17` : guillemets ouvrants ignorés (« Non, … » vaut « Non, … »).
- `factuel-04` : 735 et 736 acceptés (1 ch = 735,49875 W : troncature ou arrondi de 735,5).
- Trois items tronqués ont été relancés avec un budget supérieur avant d'être comptés en échec ; `factuel-19` (Qwen) part en boucle même à 24 000 tokens.
