# Comparatif modèles — 120 tâches françaises (OVHcloud AI Endpoints)

_Notation déterministe (regex, JSON, code exécuté, calcul exact). Aucun juge LLM._

## Synthèse

| Modèle | Note vérifiable | Items | Latence moy. | Tokens sortie | Tronqués | Erreurs | Coût /120 tâches |
|---|---|---|---|---|---|---|---|
| Olala-v1.0-mini-7A1B | **97.2 %** | 106/109 | 4.9 s | 1458 | 0 | 0 | gratuit |
| Mistral-Small-3.2-24B-Instruct-2506 | **94.5 %** | 103/109 | 4.4 s | 60 | 0 | 0 | 0.28 c$ |
| Qwen3.5-9B | **90.8 %** | 99/109 | 26.7 s | 2886 | 1 | 0 | 6.31 c$ |

## Par famille

| Famille | Olala-v1.0-mini-7A1B | Mistral-Small-3.2-24B-Instruct-2506 | Qwen3.5-9B |
|---|---|---|---|
| code | 100.0 % (19/19) | 94.7 % (18/19) | 84.2 % (16/19) |
| consignes | 100.0 % (20/20) | 75.0 % (15/20) | 95.0 % (19/20) |
| extraction | 100.0 % (20/20) | 100.0 % (20/20) | 85.0 % (17/20) |
| factuel | 90.0 % (18/20) | 100.0 % (20/20) | 85.0 % (17/20) |
| francais | 90.0 % (9/10) | 100.0 % (10/10) | 100.0 % (10/10) |
| maths | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) |

## Items discriminants

**code** — code-06, code-14, code-18
**consignes** — consignes-03, consignes-09, consignes-13, consignes-14, consignes-20
**extraction** — extraction-03, extraction-06, extraction-08
**factuel** — factuel-08, factuel-11, factuel-17, factuel-19, factuel-20
**francais** — francais-07

## Échecs communs à tous les modèles (à inspecter : checker trop strict ?)


## Échecs — Olala-v1.0-mini-7A1B (3)

- `factuel-08` — attendu 1999, lu 2005.0 — `RÉPONSE: 2005`
- `factuel-11` — attendu 240, lu 100.0 — `Le port USB‑C Power Delivery en mode PD 3.1 maximal délivre jusqu’à 100 watts. RÉPONSE: 100`
- `francais-07` — lu: Il a dit que je viendrai demain. — `Il a dit que je viendrai demain.`

## Échecs — Mistral-Small-3.2-24B-Instruct-2506 (6)

- `code-18` — 0/1 tests — ````python
def devise(n):
    return f"{n:,.2f} €"
````
- `consignes-03` — 8 mots — `Cœur électronique reliant tous les composants informatiques essentiels`
- `consignes-09` — lu: voici les noms listes par ordre alphabetique : balzac,hugo,z — `Voici les noms listés par ordre alphabétique :

Balzac, Hugo, Zola`
- `consignes-13` — 6 mots — `"Aujourd'hui, je profite du soleil printemier."`
- `consignes-14` — lu: LE PROTOCOLE SERT À RÉSOUDRE LES NOMS DE — `LE PROTOCOLE SERT À RÉSOUDRE LES NOMS DE DOMAINE EST LE DNS`
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

- Jeu de test : 120 tâches, 6 familles, hash SHA-256 `6e4e2a08327cbe4a67affc5f97bfed66d79240ce27fb33138e29f8235aff14e2` (v1.1 ; v1 corrigée, voir plus bas).
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
