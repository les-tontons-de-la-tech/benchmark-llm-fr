#!/usr/bin/env python3
"""Construit le jeu de 120 prompts FR pour le benchmark Olala mini 7A1B.

6 familles x 20 prompts. Chaque prompt porte un `checker` déterministe quand
c'est possible (format, JSON, calcul, code exécuté, réponse factuelle) ; les
familles libres sont marquées "judge" et seront notées ensuite.
"""
import json, random, pathlib

random.seed(20261121)
OUT = pathlib.Path(__file__).parent / "prompts.jsonl"
P = []

def add(fam, pid, prompt, checker, meta=None):
    P.append({"id": f"{fam}-{pid:02d}", "family": fam, "prompt": prompt,
              "checker": checker, "meta": meta or {}})

# ---------- F1 : suivi de consignes strictes (20) ----------
f1 = [
 ("Réponds uniquement par le mot OUI ou NON, sans ponctuation : la Terre est-elle plus grande que la Lune ?", {"type":"one_of","accept":["OUI","NON"],"expect":"OUI"}),
 ("Donne la liste des trois couleurs primaires en peinture, séparées par des points-virgules, sans aucun autre texte.", {"type":"exact_norm","expect":"rouge;bleu;jaune"}),
 ("Écris exactement 12 mots (ni plus ni moins) pour décrire une carte mère. Aucune liste, aucune ponctuation finale.", {"type":"wordcount","n":12}),
 ("Réponds en JSON strict, sans texte autour : {\"unite\": <string>, \"symbole\": <string>} pour l'unité de la puissance électrique.", {"type":"json_fields","expect":{"unite":"watt","symbole":"W"}}),
 ("Cite trois avantages du stockage NVMe, un par ligne, précédé d'un tiret, sans phrase d'introduction.", {"type":"bullet_lines","n":3}),
 ("Réponds en une seule phrase de moins de 20 mots qui contient le mot « souveraineté » et le mot « cloud ».", {"type":"sentence","must":["souveraineté","cloud"],"max_words":20}),
 ("Donne le résultat de 17 × 23 puis écris-le au format « RÉPONSE: <nombre> » et rien d'autre.", {"type":"final_number","expect":391}),
 ("Explique en deux phrases maximum pourquoi un SSD chauffe. Ne commence pas par « Il ».", {"type":"constraint","max_sentences":2,"forbid_start":"Il"}),
 ("Liste alphabétiquement ces trois noms, séparés par une virgule et un espace : Zola, Balzac, Hugo.", {"type":"exact_norm","expect":"balzac, hugo, zola"}),
 ("Réponds avec un unique nombre entier, sans unité ni ponctuation : combien de bits dans deux octets ?", {"type":"int","expect":16}),
 ("Reformule cette phrase au pluriel, sans rien ajouter : « Le serveur est lent. »", {"type":"exact_norm","expect":"les serveurs sont lents"}),
 ("Donne trois synonymes de « rapide » sur une seule ligne séparés par « / », sans autre texte.", {"type":"count_sep","sep":"/","n":3}),
 ("Écris une phrase de 8 mots exactement qui commence par « Aujourd'hui ».", {"type":"starts_wordcount","start":"aujourd'hui","n":8}),
 ("Réponds en MAJUSCULES uniquement, sans ponctuation : quel protocole sert à résoudre les noms de domaine ?", {"type":"uppercase","expect":"DNS"}),
 ("Donne un JSON strict sans texte autour : une liste « notes » de trois nombres (3, 12, 7) triés croissants.", {"type":"json_list","key":"notes","expect":[3,7,12]}),
 ("En une seule ligne, écris la conversion : 1 Go = … Mo (chiffre seul attendu après le signe égal).", {"type":"final_number","expect":1024}),
 ("Réponds par une phrase affirmative à la forme négative correcte : « Tu as vu le câble ? » — commence par « Non ».", {"type":"starts","start":"non"}),
 ("Donne le nom du composant qui convertit le courant alternatif en continu, en deux mots maximum, sans article.", {"type":"max_words","n":2,"expect_contains":"alimentation"}),
 ("Écris exactement la chaîne « OK-2026 » suivie d'un espace puis de la somme de 40 et 2.", {"type":"regex","pattern":"^OK-2026 42$"}),
 ("Classe ces températures de la plus froide à la plus chaude, séparées par « < » : 12°C, -3°C, 7°C.", {"type":"exact_norm","expect":"-3°c<7°c<12°c"}),
]
for i,(pr,ck) in enumerate(f1,1): add("consignes", i, pr, ck)

# ---------- F2 : extraction structurée (20) ----------
docs = [
 ("Le serveur Dell R760 du site de Roubaix a été livré le 12 mars 2026 pour 14 250 euros HT. Il est garanti 36 mois.", {"modele":"R760","site":"Roubaix","prix_ht":14250,"garantie_mois":36}),
 ("La baie NetApp AFF A250, installée à Lille le 3 juin 2026, a coûté 87 900 euros HT avec 5 ans de support.", {"modele":"AFF A250","site":"Lille","prix_ht":87900,"garantie_mois":60}),
 ("Switch Cisco Catalyst 9300 livré le 28 janvier 2026 à Nantes pour 6 480 euros HT, garantie 12 mois.", {"modele":"Catalyst 9300","site":"Nantes","prix_ht":6480,"garantie_mois":12}),
 ("Deux hyperviseurs HPE DL380 Gen11 commandés le 9 septembre 2026 pour Bordeaux : 31 700 euros HT au total, support 24 mois.", {"modele":"DL380 Gen11","site":"Bordeaux","prix_ht":31700,"garantie_mois":24}),
 ("Le nas Synology RS4021xs+ de Strasbourg a été facturé 9 150 euros HT le 17 avril 2026, garantie 5 ans.", {"modele":"RS4021xs+","site":"Strasbourg","prix_ht":9150,"garantie_mois":60}),
 ("Poste de travail HP Z4 G5, Lyon, 4 300 euros HT, livré le 22 février 2026, garantie 36 mois.", {"modele":"Z4 G5","site":"Lyon","prix_ht":4300,"garantie_mois":36}),
 ("Firewall Fortinet 200F déployé à Toulouse le 5 novembre 2026 pour 12 900 euros HT, licence 3 ans.", {"modele":"200F","site":"Toulouse","prix_ht":12900,"garantie_mois":36}),
 ("Le cluster GPU de Grenoble (8 × L40S) a été livré le 30 juillet 2026, 412 000 euros HT, support 12 mois.", {"modele":"L40S","site":"Grenoble","prix_ht":412000,"garantie_mois":12}),
 ("Onduleur APC Smart-UPS SRT de Marseille, 5 700 euros HT, installé le 14 mai 2026, garantie 24 mois.", {"modele":"SRT","site":"Marseille","prix_ht":5700,"garantie_mois":24}),
 ("Routeur Juniper MX204 à Rennes : 18 300 euros HT, mise en service le 8 août 2026, garantie 48 mois.", {"modele":"MX204","site":"Rennes","prix_ht":18300,"garantie_mois":48}),
 ("Le SAN Pure Storage FlashArray //X20 de Montpellier a coûté 156 400 euros HT, livré le 2 octobre 2026, support 36 mois.", {"modele":"FlashArray //X20","site":"Montpellier","prix_ht":156400,"garantie_mois":36}),
 ("Station d'archivage Quantum Scalar i3 à Nancy, 22 800 euros HT, livrée le 19 décembre 2026, garantie 60 mois.", {"modele":"Scalar i3","site":"Nancy","prix_ht":22800,"garantie_mois":60}),
 ("Switch Arista 7050X4 pour le site de Dijon, 27 500 euros HT, commandé le 11 janvier 2026, garantie 36 mois.", {"modele":"7050X4","site":"Dijon","prix_ht":27500,"garantie_mois":36}),
 ("Contrôleur Wi-Fi Cisco 9800-L à Angers, 8 900 euros HT, installé le 26 septembre 2026, support 24 mois.", {"modele":"9800-L","site":"Angers","prix_ht":8900,"garantie_mois":24}),
 ("Le serveur Supermicro AS-2015HS de Brest a été livré le 6 juin 2026 pour 19 750 euros HT, garantie 12 mois.", {"modele":"AS-2015HS","site":"Brest","prix_ht":19750,"garantie_mois":12}),
 ("Sauvegarde Veeam sur baie HPE MSA 2062 à Tours, 33 200 euros HT, livrée le 23 mars 2026, garantie 48 mois.", {"modele":"MSA 2062","site":"Tours","prix_ht":33200,"garantie_mois":48}),
 ("Point d'accès Ubiquiti U7 Pro à Clermont-Ferrand, 1 240 euros HT, déployé le 15 février 2026, garantie 12 mois.", {"modele":"U7 Pro","site":"Clermont-Ferrand","prix_ht":1240,"garantie_mois":12}),
 ("Baie Dell PowerStore 500T à Metz, 98 600 euros HT, livrée le 4 décembre 2026, support 60 mois.", {"modele":"PowerStore 500T","site":"Metz","prix_ht":98600,"garantie_mois":60}),
 ("Le kiosque de recette Supermicro de La Rochelle, 2 900 euros HT, livré le 12 octobre 2026, garantie 24 mois.", {"modele":"Supermicro","site":"La Rochelle","prix_ht":2900,"garantie_mois":24}),
 ("Switch MikroTik CRS520 à Ajaccio, 3 450 euros HT, installé le 29 août 2026, garantie 36 mois.", {"modele":"CRS520","site":"Ajaccio","prix_ht":3450,"garantie_mois":36}),
]
for i,(doc,truth) in enumerate(docs,1):
    pr = ("Extrais les informations de ce texte et réponds en JSON strict, sans texte autour, avec exactement "
          "ces clés : modele, site, prix_ht (entier, sans espace ni devise), garantie_mois (entier).\n\n" + doc)
    add("extraction", i, pr, {"type":"json_fields","expect":truth})

# ---------- F3 : arithmétique / raisonnement numérique (20) ----------
arith = []
for i in range(10):
    a,b = random.randint(37,198), random.randint(11,29)
    arith.append((f"Un serveur consomme {a} W en charge et {b} W au repos. Combien de watts économise-t-on en passant du repos à la charge ? Termine par « RÉPONSE: <nombre> ».", a-b))
for i in range(5):
    p,q,n = random.randint(1200,4800), random.randint(3,9), random.randint(2,24)
    arith.append((f"Un lot de {n} serveurs coûte {p} euros l'unité, avec {q}% de remise. Quel est le prix total après remise, en euros ? Termine par « RÉPONSE: <nombre arrondi à l'entier> ».", round(p*n*(1-q/100))))
for i in range(5):
    tot,part = random.randint(24,96), random.randint(3,11)
    arith.append((f"Un budget de {tot} 000 euros est réparti à parts égales entre {part} projets. Combien d'euros par projet ? Termine par « RÉPONSE: <nombre> ».", round(tot*1000/part)))
for i,(pr,ans) in enumerate(arith,1):
    add("maths", i, pr, {"type":"final_number","expect":ans})

# ---------- F4 : code (20) ----------
code = [
 ("Écris une fonction Python `somme_pairs(n)` qui renvoie la somme des entiers pairs de 0 à n inclus. Réponds uniquement avec le bloc de code.", {"fn":"somme_pairs","tests":[[(10,),30],[(0,),0],[(7,),12]]}),
 ("Écris une fonction Python `inverse(mot)` qui renvoie la chaîne inversée. Réponds uniquement avec le bloc de code.", {"fn":"inverse","tests":[[("abc",),"cba"],[("",),""]]}),
 ("Écris une fonction Python `compter_voyelles(s)` qui compte les voyelles (a,e,i,o,u,y) sans tenir compte de la casse. Réponds uniquement avec le bloc de code.", {"fn":"compter_voyelles","tests":[[("Bonjour",),3],[("XYZ",),1],[("",),0]]}),
 ("Écris une fonction Python `max_liste(l)` qui renvoie le plus grand élément sans utiliser `max`. Réponds uniquement avec le bloc de code.", {"fn":"max_liste","tests":[[([3,9,2],),9],[([-5,-1,-9],),-1]]}),
 ("Écris une fonction Python `est_palindrome(s)` qui ignore casse et espaces. Réponds uniquement avec le bloc de code.", {"fn":"est_palindrome","tests":[[("Elu par cette crapule",),True],[("abc",),False]]}),
 ("Écris une fonction Python `fizzbuzz(n)` qui renvoie une liste de 1 à n avec Fizz, Buzz, FizzBuzz. Réponds uniquement avec le bloc de code.", {"fn":"fizzbuzz","tests":[[(5,),["1","2","Fizz","4","Buzz"]]]}),
 ("Écris une fonction Python `moyenne(l)` qui renvoie la moyenne d'une liste non vide, arrondie à 2 décimales. Réponds uniquement avec le bloc de code.", {"fn":"moyenne","tests":[[([1,2,4],),2.33],[([10],),10.0]]}),
 ("Écris une fonction Python `mots_uniques(phrase)` qui renvoie l'ensemble des mots en minuscules. Réponds uniquement avec le bloc de code.", {"fn":"mots_uniques","tests":[[("Le chat le Chat",),["chat","le"]]]}),
 ("Écris une fonction Python `facteur(n)` qui renvoie n! pour n >= 0. Réponds uniquement avec le bloc de code.", {"fn":"facteur","tests":[[(5,),120],[(0,),1]]}),
 ("Écris une fonction Python `tri_bulles(l)` qui trie une liste d'entiers par tri à bulles et la renvoie. Réponds uniquement avec le bloc de code.", {"fn":"tri_bulles","tests":[[([3,1,2],),[1,2,3]]]}),
 ("Écris une fonction Python `fib(n)` qui renvoie le n-ième terme de Fibonacci (fib(0)=0). Réponds uniquement avec le bloc de code.", {"fn":"fib","tests":[[(10,),55],[(1,),1]]}),
 ("Écris une fonction Python `verifier_ip(s)` qui renvoie True si la chaîne est une IPv4 valide, sinon False. Réponds uniquement avec le bloc de code.", {"fn":"verifier_ip","tests":[[("192.168.1.1",),True],[("256.1.1.1",),False]]}),
 ("Écris une fonction Python `freq_chars(s)` qui renvoie un dictionnaire des fréquences de caractères. Réponds uniquement avec le bloc de code.", {"fn":"freq_chars","tests":[[("aab",),{"a":2,"b":1}]]}),
 ("Écris une fonction Python `convertir_octets(n)` qui convertit un nombre d'octets en Ko, Mo ou Go (1 Ko = 1024). Réponds uniquement avec le bloc de code.", {"fn":"convertir_octets","tests":[[(2048,),("2.0 Ko")],[(1048576,),("1.0 Mo")]]}),
 ("Écris une fonction Python `anagramme(a,b)` qui dit si deux mots sont anagrammes (casse ignorée). Réponds uniquement avec le bloc de code.", {"fn":"anagramme","tests":[[("chien","niche"),True],[("abc","abd"),False]]}),
 ("Écris une fonction Python `lire_csv(texte)` qui transforme un CSV à deux colonnes en dictionnaire. Réponds uniquement avec le bloc de code.", {"fn":"lire_csv","tests":[[("a,b\\n1,2",),{"a":"1","b":"2"}]]}),
 ("Écris une fonction Python `dichotomie(l, x)` qui renvoie l'index de x dans une liste triée ou -1. Réponds uniquement avec le bloc de code.", {"fn":"dichotomie","tests":[[([1,3,5,7],5),2],[([1,3],9),-1]]}),
 ("Écris une fonction Python `devise(n)` qui formate un nombre avec espace des milliers et « € ». Réponds uniquement avec le bloc de code.", {"fn":"devise","tests":[[(14250,),"14 250 €"]]}),
 ("Écris une fonction Python `supprimer_doublons(l)` qui garde l'ordre d'apparition. Réponds uniquement avec le bloc de code.", {"fn":"supprimer_doublons","tests":[[([1,2,1,3],),[1,2,3]]]}),
 ("Écris une fonction Python `est_premier(n)` qui renvoie True si n est premier. Réponds uniquement avec le bloc de code.", {"fn":"est_premier","tests":[[(7,),True],[(9,),False],[(1,),False]]}),
]
for i,(pr,ck) in enumerate(code,1): add("code", i, pr, {"type":"python","expect":ck})

# ---------- F5 : français / langue (20) ----------
fr = [
 ("Accorde correctement et réponds uniquement par la phrase corrigée : « Les rapport que j'ai reçu sont incomplet. »", "judge"),
 ("Réponds uniquement par la forme correcte : « Je me suis rendu compte » ou « Je me suis rendu comptes » ?", "judge"),
 ("Donne le participe passé correct : « Elle a (résoudre) le problème. » — réponds uniquement par la forme verbale.", "judge"),
 ("Réécris cette phrase sans faute : « Malgré que ce soit cher, on va le prendre. »", "judge"),
 ("Explique en une phrase la différence entre « censé » et « sensé ».", "judge"),
 ("Réponds uniquement par le mot correct : « un » ou « une » devant « astérisque », « oasis », « été ».", "judge"),
 ("Corrige la ponctuation : « Il a dit je viendrai demain » — réponds uniquement par la phrase corrigée.", "judge"),
 ("Remplace « faire » par un verbe plus précis dans : « Il fait une erreur. » — un seul verbe attendu.", "judge"),
 ("Réponds uniquement par la forme correcte : « davantage » ou « d'avantage » dans « il en faut ___ ».", "judge"),
 ("Réécris cette phrase au style direct : « Il m'a demandé si je viendrais. »", "judge"),
 ("Donne l'antonyme de « prolixe » en un mot.", "judge"),
 ("Explique en deux phrases maximum la règle de l'accord du participe passé avec « avoir ».", "judge"),
 ("Réponds uniquement par le mot correct : « a » ou « à » — « Il ___ décidé de partir ___ Lyon. »", "judge"),
 ("Transforme en voix passive : « Le technicien a remplacé le disque. »", "judge"),
 ("Donne un exemple de phrase contenant un complément d'objet indirect, et souligne-le entre crochets.", "judge"),
 ("Réponds uniquement par la forme correcte : « quoique » ou « quoi que » dans « ___ tu fasses ».", "judge"),
 ("Corrige : « Les données que j'ai analysées sont fiable. »", "judge"),
 ("Écris en toutes lettres le nombre 140 250 correctement orthographié.", "judge"),
 ("Réécris sans répétition : « Le serveur est lent, le serveur est vieux, le serveur chauffe. »", "judge"),
 ("Donne trois mots de la même famille que « numérique », séparés par des virgules.", "judge"),
]
for i,(pr,ck) in enumerate(fr,1): add("francais", i, pr, ck)

# ---------- F6 : factuel vérifiable (20) ----------
fact = [
 ("Quelle est la consommation électrique typique d'une RTX 4090, en watts (valeur officielle du TDP) ? Termine par « RÉPONSE: <nombre> ».", 450),
 ("Combien de bits contient une adresse IPv6 ? Termine par « RÉPONSE: <nombre> ».", 128),
 ("En quelle année la loi de Moore a-t-elle été formulée ? Termine par « RÉPONSE: <année> ».", 1965),
 ("Combien de watts vaut 1 cheval-vapeur métrique (arrondi à l'entier) ? Termine par « RÉPONSE: <nombre> ».", 736),
 ("Quel est le port TCP standard d'HTTPS ? Termine par « RÉPONSE: <nombre> ».", 443),
 ("Combien de cœurs compte un Ryzen 9 7950X ? Termine par « RÉPONSE: <nombre> ».", 16),
 ("Quelle est la tension nominale d'une prise domestique en France, en volts ? Termine par « RÉPONSE: <nombre> ».", 230),
 ("En quelle année OVHcloud a-t-elle été fondée ? Termine par « RÉPONSE: <année> ».", 1999),
 ("Combien de nanomètres dans un micromètre ? Termine par « RÉPONSE: <nombre> ».", 1000),
 ("Quelle est la capacité maximale théorique d'une adresse IPv4, en nombre d'adresses (puissance de 2) ? Termine par « RÉPONSE: 2^<exposant> ».", None),
 ("Combien de watts consomme un port USB-C Power Delivery en profil maximal (PD 3.1) ? Termine par « RÉPONSE: <nombre> ».", 240),
 ("Quelle est la température d'ébullition de l'eau au niveau de la mer, en degrés Celsius ? Termine par « RÉPONSE: <nombre> ».", 100),
 ("Combien de bits dans un octet ? Termine par « RÉPONSE: <nombre> ».", 8),
 ("Quel est le nom du protocole de routage utilisé par Internet depuis 1993 ? Termine par « RÉPONSE: <nom> ».", None),
 ("Quelle fréquence maximale utilise le Wi-Fi 7 sur la bande 6 GHz, en GHz ? Termine par « RÉPONSE: <nombre> ».", 6),
 ("Combien de couches compte le modèle OSI ? Termine par « RÉPONSE: <nombre> ».", 7),
 ("En quelle année a été publié le premier standard USB ? Termine par « RÉPONSE: <année> ».", 1996),
 ("Combien de grammes pèse un litre d'eau à 4 °C ? Termine par « RÉPONSE: <nombre> ».", 1000),
 ("Quelle est la vitesse de la lumière dans le vide, arrondie, en km/s ? Termine par « RÉPONSE: <nombre> ».", 300000),
 ("Combien de PCIe lanes expose un CPU AM5 grand public de la série Ryzen 7000 au total, côté CPU ? Termine par « RÉPONSE: <nombre> ».", 28),
]
for i,(pr,ans) in enumerate(fact,1):
    ck = {"type":"final_number","expect":ans} if ans is not None else {"type":"judge"}
    add("factuel", i, pr, ck)

with OUT.open("w", encoding="utf-8") as f:
    for p in P: f.write(json.dumps(p, ensure_ascii=False) + "\n")
print(f"{len(P)} prompts écrits dans {OUT}")
from collections import Counter
print(Counter(p["family"] for p in P))
print(Counter(p["checker"] if isinstance(p["checker"],str) else p["checker"]["type"] for p in P))
