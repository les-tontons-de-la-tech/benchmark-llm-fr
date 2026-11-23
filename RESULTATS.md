# Comparatif modèles — 120 tâches françaises (OVHcloud AI Endpoints)

_Notation déterministe pour 109 items (regex, JSON, code exécuté, calcul exact) ; 8 items de rédaction libre jugés par Claude Opus 5.5, à température 0, sur critères publiés (voir `judge_criteria.json`) — juge hors compétition._

## Synthèse

| Modèle | Note vérifiable | Items | Latence moy. | Tokens sortie | Tronqués | Erreurs | Coût /120 tâches |
|---|---|---|---|---|---|---|---|
| gemma-4-26b-a4b | **98.3 %** | 115/117 | 8.3 s | 1127 | 0 | 0 | 5.61 c$ |
| Qwen3.5-397B-A17B | **98.3 %** | 115/117 | 14.4 s | 2313 | 1 | 0 | 118.38 c$ |
| Qwen3.6-27B | **98.3 %** | 115/117 | 7.8 s | 1108 | 0 | 0 | 42.72 c$ |
| gpt-oss-120b | **97.4 %** | 114/117 | 2.9 s | 212 | 0 | 0 | 1.31 c$ |
| Qwen3.8-27B | **97.4 %** | 114/117 | 6.0 s | 621 | 0 | 0 | 24.29 c$ |
| nemotron3-omni-30b | **96.6 %** | 113/117 | 2.5 s | 383 | 0 | 0 | 2.76 c$ |
| DeepSeek-V4.1-Flash-1017 | **95.7 %** | 112/117 | 1.6 s | 302 | 0 | 0 | 4.80 c$ |
| nemotron3-nano-30b | **95.7 %** | 112/117 | 1.8 s | 329 | 0 | 0 | 0.95 c$ |
| Qwen2.5-VL-72B-Instruct | **95.7 %** | 112/117 | 2.0 s | 66 | 0 | 0 | 1.58 c$ |
| qwen3.6-35b-a3b | **95.7 %** | 112/117 | 14.0 s | 2035 | 3 | 0 | 32.60 c$ |
| gpt-oss-20b | **94.9 %** | 111/117 | 2.3 s | 270 | 0 | 0 | 0.65 c$ |
| laguna-xs-2.1 | **94.9 %** | 111/117 | 5.4 s | 729 | 0 | 0 | 1.11 c$ |
| Meta-Llama-3_3-70B-Instruct | **94.9 %** | 111/117 | 2.8 s | 79 | 0 | 0 | 1.40 c$ |
| qwen3-vl-30b-a3b | **94.9 %** | 111/117 | 1.3 s | 157 | 0 | 0 | 1.19 c$ |
| Olala-v1.0-mini-7A1B | **94.0 %** | 110/117 | 4.9 s | 1458 | 0 | 0 | gratuit |
| Mistral-Small-3.2-24B-Instruct-2506 | **92.3 %** | 108/117 | 4.4 s | 60 | 0 | 0 | 0.28 c$ |
| Qwen3.5-9B | **92.3 %** | 108/117 | 26.7 s | 2886 | 1 | 0 | 6.31 c$ |

## Par famille

| Famille | gemma-4-26b-a4b | Qwen3.5-397B-A17B | Qwen3.6-27B | gpt-oss-120b | Qwen3.8-27B | nemotron3-omni-30b | DeepSeek-V4.1-Flash-1017 | nemotron3-nano-30b | Qwen2.5-VL-72B-Instruct | qwen3.6-35b-a3b | gpt-oss-20b | laguna-xs-2.1 | Meta-Llama-3_3-70B-Instruct | qwen3-vl-30b-a3b | Olala-v1.0-mini-7A1B | Mistral-Small-3.2-24B-Instruct-2506 | Qwen3.5-9B |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| code | 94.7 % (18/19) | 100.0 % (19/19) | 94.7 % (18/19) | 100.0 % (19/19) | 100.0 % (19/19) | 89.5 % (17/19) | 100.0 % (19/19) | 94.7 % (18/19) | 100.0 % (19/19) | 100.0 % (19/19) | 100.0 % (19/19) | 100.0 % (19/19) | 94.7 % (18/19) | 94.7 % (18/19) | 100.0 % (19/19) | 94.7 % (18/19) | 89.5 % (17/19) |
| consignes | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 95.0 % (19/20) | 100.0 % (20/20) | 100.0 % (20/20) | 95.0 % (19/20) | 100.0 % (20/20) | 85.0 % (17/20) | 100.0 % (20/20) | 100.0 % (20/20) | 90.0 % (18/20) | 95.0 % (19/20) | 85.0 % (17/20) | 100.0 % (20/20) | 75.0 % (15/20) | 95.0 % (19/20) |
| extraction | 100.0 % (20/20) | 95.0 % (19/20) | 100.0 % (20/20) | 95.0 % (19/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 95.0 % (19/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 85.0 % (17/20) |
| factuel | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 95.0 % (19/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 95.0 % (19/20) | 85.0 % (17/20) | 95.0 % (19/20) | 100.0 % (20/20) | 100.0 % (20/20) | 90.0 % (18/20) | 100.0 % (20/20) | 85.0 % (17/20) |
| francais | 94.4 % (17/18) | 94.4 % (17/18) | 94.4 % (17/18) | 94.4 % (17/18) | 100.0 % (18/18) | 88.9 % (16/18) | 100.0 % (18/18) | 77.8 % (14/18) | 100.0 % (18/18) | 94.4 % (17/18) | 100.0 % (18/18) | 83.3 % (15/18) | 83.3 % (15/18) | 88.9 % (16/18) | 72.2 % (13/18) | 83.3 % (15/18) | 100.0 % (18/18) |
| maths | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 90.0 % (18/20) | 100.0 % (20/20) | 80.0 % (16/20) | 100.0 % (20/20) | 95.0 % (19/20) | 85.0 % (17/20) | 85.0 % (17/20) | 100.0 % (20/20) | 95.0 % (19/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) | 100.0 % (20/20) |

## Items discriminants

**code** — code-14, code-17, code-18
**consignes** — consignes-03, consignes-09, consignes-13, consignes-14, consignes-18, consignes-20
**extraction** — extraction-03, extraction-06, extraction-08, extraction-16
**factuel** — factuel-04, factuel-08, factuel-11, factuel-17, factuel-19, factuel-20
**francais** — francais-04, francais-07, francais-08, francais-10, francais-12, francais-15, francais-16, francais-19, francais-20
**maths** — maths-02, maths-03, maths-04, maths-05, maths-08, maths-10, maths-11

## Échecs communs à tous les modèles (à inspecter : checker trop strict ?)


## Échecs — gemma-4-26b-a4b (2)

- `code-18` — 0/1 tests — ````python
def devise(n):
    return f"{n:,.2f}".replace(",", " ").replace(".", ",") + " €"
````
- `francais-19` — juge Claude : KO — `Voici plusieurs options selon la nuance que vous souhaitez donner :

**La plus simple et directe :**
> « Le se`

## Échecs — Qwen3.5-397B-A17B (2)

- `extraction-03` — champs ['modele', 'site', 'prix_ht', 'garantie_mois'] — `{
  "modele": "Switch Cisco Catalyst 9300",
  "site": null,
  "prix_ht": 6480,
  "garantie_mois": 12
}`
- `francais-08` — juge Claude : KO — ``

## Échecs — Qwen3.6-27B (2)

- `code-18` — 0/1 tests — ````python
def devise(n):
    return f"{n:_} €"
````
- `francais-19` — juge Claude : KO — `Voici une version fluide et sans répétition :

**« Le serveur est lent, vieux et chauffe. »**

💡 *Note de st`

## Échecs — gpt-oss-120b (3)

- `consignes-20` — lu: -3 °c<7 °c<12 °c — `-3 °C < 7 °C < 12 °C`
- `extraction-16` — champs ['modele', 'site', 'prix_ht', 'garantie_mois'] — `{
  "modele": "Veeam",
  "site": "Tours",
  "prix_ht": 33200,
  "garantie_mois": 48
}`
- `francais-16` — manquants: [['quoi que']] — `quoique`

## Échecs — Qwen3.8-27B (3)

- `factuel-20` — attendu [24, 28], lu 20.0 — `Le CPU AM5 grand public de la série Ryzen 7000 expose 20 lanes PCIe directement côté CPU.

RÉPONSE: 20`
- `maths-05` — attendu 22, lu -22.0 — `En passant du repos (16 W) à la charge (38 W), la consommation augmente de 22 W, donc l’économie est négativ`
- `maths-10` — attendu 111, lu -111.0 — `En passant du repos à la charge, la consommation augmente de 111 W, donc l’économie est négative.

RÉPONSE:`

## Échecs — nemotron3-omni-30b (4)

- `code-17` — 0/2 tests — ````python
def dichotomy(l, x):
    low, high = 0, len(l) - 1
    while low <= high:
        mid = (low + high`
- `code-18` — 0/1 tests — ````python
def devise(n):
    # Convert to integer to handle possible float input
    num = int(n)
    # Forma`
- `francais-07` — lu: Il a dit, je viendrai demain — `Il a dit, je viendrai demain`
- `francais-12` — juge Claude : KO — `Avec « avoir », le participe passé s’accorde uniquement avec le COD placé avant le verbe ; s’il n’y a pas de`

## Échecs — DeepSeek-V4.1-Flash-1017 (5)

- `consignes-13` — 10 mots — `« Aujourd'hui, je mange une pomme vraiment très mûre. »`
- `maths-03` — attendu 179, lu -179.0 — `En passant du repos à la charge, la consommation augmente de 192 − 13 = 179 W. L’économie est donc négative :`
- `maths-05` — attendu 22, lu 0.0 — `En passant du repos à la charge, la consommation augmente de 22 W ; on n’économise donc rien.

RÉPONSE: 0`
- `maths-08` — attendu 57, lu -57.0 — `En passant du repos à la charge, la consommation augmente de 79 − 22 = 57 W, donc l’économie est de −57 W.

RÉ`
- `maths-10` — attendu 111, lu -111.0 — `En passant du repos (14 W) à la charge (125 W), la consommation augmente de 111 W. On n’économise donc rien :`

## Échecs — nemotron3-nano-30b (5)

- `code-18` — 0/1 tests — ````python
def devise(n):
    return f"{n:n}".replace(",", " ") + " €"
````
- `francais-04` — juge Claude : KO — `« Malheureusement, il est cher, mais nous allons le prendre. »  

ou, plus simplement :  

« Malgré qu’il soi`
- `francais-10` — juge Claude : KO — `Viendras-tu ?`
- `francais-12` — juge Claude : KO — `Avec l’auxiliaire **avoir**, le participe passé ne s’accorde jamais avec le sujet ; il ne s’accorde que s’il`
- `francais-15` — juge Claude : KO — `Il a envoyé la lettre à _[à Pierre]_.`

## Échecs — Qwen2.5-VL-72B-Instruct (5)

- `consignes-03` — 9 mots — `Composant central connecte processeurs mémoire et autres périphériques essentiels`
- `consignes-13` — 7 mots — `Aujourd'hui, le soleil brille sur notre ville.`
- `consignes-18` — 2 mots — `Rectifieur électrique`
- `extraction-16` — champs ['modele', 'site', 'prix_ht', 'garantie_mois'] — `{
"modele":"Veeam",
"site":"Tours",
"prix_ht":33200,
"garantie_mois":48
}`
- `maths-11` — attendu 8280, lu 8264.0 — `Pour calculer le prix total après remise pour un lot de 4 serveurs, nous devons suivre ces étapes:

1. Calcule`

## Échecs — qwen3.6-35b-a3b (5)

- `factuel-19` — attendu [299792, 300000], lu None — ``
- `francais-19` — juge Claude : KO — `« Le serveur est lent, ancien et surchauffe. »`
- `maths-02` — attendu 86, lu None — ``
- `maths-08` — attendu 57, lu -57.0 — `Pour déterminer la quantité de watts économisés, il faut calculer la différence entre la consommation initia`
- `maths-10` — attendu 111, lu None — ``

## Échecs — gpt-oss-20b (6)

- `factuel-04` — attendu [735, 736], lu 75000.0 — `RÉPONSE: 75000`
- `factuel-11` — attendu 240, lu 100.0 — `RÉPONSE: 100`
- `factuel-20` — attendu [24, 28], lu 64.0 — `RÉPONSE: 64`
- `maths-04` — attendu 110, lu 0.0 — `En passant du repos à la charge, le serveur consomme 123 W au lieu de 13 W, soit 110 W de plus. On ne réalise`
- `maths-05` — attendu 22, lu -22.0 — `RÉPONSE: -22.`
- `maths-10` — attendu 111, lu 0.0 — `RÉPONSE: 0`

## Échecs — laguna-xs-2.1 (6)

- `consignes-18` — 2 mots — `Bridge rectifier`
- `consignes-20` — lu: les temperatures classees de la plus froide a la plus chaude — `Les températures classées de la plus froide à la plus chaude sont :  
**-3°C < 7°C < 12°C**`
- `factuel-19` — attendu [299792, 300000], lu 300.0 — `La vitesse de la lumière dans le vide est définie exactement comme étant 299 792,458 mètres par seconde. Pour`
- `francais-08` — juge Claude : KO — `**Réponse :**  
« Il **commet** une erreur. »  

Le verbe **commettre** (ou **cometer**) est plus précis et id`
- `francais-10` — juge Claude : KO — `**Phrase réécrite au style direct :**  
« Il m'a demandé si je viens. »  

**Explication :**  
Le style direct`
- `francais-12` — juge Claude : KO — `Le participe passé s'accorde en genre et en nombre avec le sujet lorsqu'il est précédé de "avoir". Il s'accord`

## Échecs — Meta-Llama-3_3-70B-Instruct (6)

- `code-18` — 0/1 tests — ````python
def devise(n):
    return "{:,.2f} €".format(n).replace(",", " ").replace(".", ",")

# Exemple d'uti`
- `consignes-14` — lu: LE PROTOCOLE DNS SERVIRA A RESOUDRE LES  — `LE PROTOCOLE DNS SERVIRA A RESOUDRE LES NOMS DE DOMAINES EN ADRESSES IP`
- `francais-08` — juge Claude : KO — `Commets`
- `francais-12` — juge Claude : KO — `Lorsqu'un verbe est conjugué avec "avoir", le participe passé s'accorde en genre et en nombre avec l'objet dir`
- `francais-19` — juge Claude : KO — `Voici une version sans répétition : « Le serveur est lent, vieux et chauffe. »`
- `maths-11` — attendu 8280, lu 8279.0 — `Pour calculer le prix total après remise, nous devons d’abord calculer le prix d’un serveur après remise, puis`

## Échecs — qwen3-vl-30b-a3b (6)

- `code-17` — 0/2 tests — ````python
def dichotomie(l, x):
    gauche, droit = 0, len(l) - 1
    while gauche <= droit:
        milieu =`
- `consignes-03` — 22 mots — `Carte mère connecte composants gère flux données supporte processeur mémoire ports buses électronique intégrée`
- `consignes-13` — 7 mots — `Aujourd'hui, le soleil brille dans le ciel.`
- `consignes-20` — lu: pour classer les temperatures de la plus froide a la plus ch — `Pour classer les températures de la plus froide à la plus chaude, on compare les valeurs numériques :

-3°C es`
- `francais-15` — juge Claude : KO — `J’**envoie** [une lettre à mon ami] tous les jours.  

Le complément d'objet indirect est **[une lettre à mon`
- `francais-19` — juge Claude : KO — `Le serveur est lent, vieux et surchauffe.`

## Échecs — Olala-v1.0-mini-7A1B (7)

- `factuel-08` — attendu 1999, lu 2005.0 — `RÉPONSE: 2005`
- `factuel-11` — attendu 240, lu 100.0 — `Le port USB‑C Power Delivery en mode PD 3.1 maximal délivre jusqu’à 100 watts. RÉPONSE: 100`
- `francais-07` — lu: Il a dit que je viendrai demain. — `Il a dit que je viendrai demain.`
- `francais-10` — juge Claude : KO — `La phrase « Il m'a demandé si je viendrais » est déjà exprimée de manière directe en français. Cependant, si l`
- `francais-12` — juge Claude : KO — `Le participe passé s’accorde en genre et en nombre avec le complément d’objet direct lorsqu’on l’utilise avec`
- `francais-19` — juge Claude : KO — `Le serveur devient lent, vieilli et chaud.`
- `francais-20` — juge Claude : KO — `digitale, informatique, électronique`

## Échecs — Mistral-Small-3.2-24B-Instruct-2506 (9)

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
- `francais-15` — juge Claude : KO — `Voici un exemple de phrase contenant un complément d'objet indirect (souligné entre croches) :

*Je parle [à m`
- `francais-19` — juge Claude : KO — `Voici quelques reformulations sans répétition :

1. « Le serveur est lent, il est aussi ancien et surchauffe.`
- `francais-20` — juge Claude : KO — `Voici trois mots de la même famille que « numérique » :

**numérisation, numériser, digital**`

## Échecs — Qwen3.5-9B (9)

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
