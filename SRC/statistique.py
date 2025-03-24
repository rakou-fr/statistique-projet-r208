import asyncio
import matplotlib.pyplot as plt
import numpy as np
import os
import json

## Variable global
listePrixMagasin = [199, 119, 49]


## Initialiseurs
async def chargerJson():
    '''
    Entrée : 
    Sortie : liste contenant les JSONs chargés
    '''
    lesJsons = ["./SRC/JSON/RL.json", "./SRC/JSON/Corteiz.json", "./SRC/JSON/H&M.json"]
    retourJson = []
    for path in lesJsons:
        try:
            with open(path, "r", encoding="utf8") as fichier:
                retourJson.append(json.load(fichier))
        except FileNotFoundError:
            print(f"Fichier non trouvé : {path}")
    return retourJson 

async def chargerPrix(listeJson):
    '''
    Entrée : liste de JSONs
    Sortie : liste de listes contenant les prix de chaque JSON
    '''
    prix_par_json = [] 

    for json_data in listeJson:
        prix = []
        if "items" in json_data:
            for item in json_data["items"]:
                prix.append(float(item["price"]["amount"]))
        prix_par_json.append(prix) 

    return prix_par_json

async def chargerFavoris(listeJson):
    '''
    Entrée : liste de JSONs
    Sortie : liste de listes contenant les favorite_count de chaque JSON
    '''
    favoris_par_json = []  

    for json_data in listeJson:
        favoris = []
        if "items" in json_data:
            for item in json_data["items"]:
                favorite_count = item.get("favorite_count") or item.get("favourite_count", 0)
                favoris.append(int(favorite_count))
        favoris_par_json.append(favoris)
    return favoris_par_json


## Statistiques

async def moyenne (Liste) :
    moyenne = []
    for x in range(len(Liste)):
        moyenne.append(np.mean(Liste[x]).tolist())
    return moyenne

async def mediane (liste) :
    mediane = []
    for x in range(len(liste)):
        mediane.append(np.median(liste[x]).tolist())
    return mediane

async def ecart_type (liste) :
    ecart_type = []
    for x in range(len(liste)):
        ecart_type.append(np.std(liste[x]).tolist())
    return ecart_type

async def quartiles (liste) :
    q1 = []
    q2 = []
    q3 = []
    for x in range(len(liste)):
        q1.append(np.quantile(liste[x],0.25, method = 'midpoint').tolist())
        q2.append(np.quantile(liste[x],0.50, method = 'midpoint').tolist())
        q3.append(np.quantile(liste[x],0.75, method = 'midpoint').tolist())
    return q1, q2, q3

async def effectifs (liste) :
    modalités = []
    effectifs = []
    for x in range(len(liste)):
        modalités.append(np.unique(liste[x]).tolist())
        effectifs.append(np.size(liste[x]))
    return modalités, effectifs


async def frequences (liste) :
    frequences = []
    for x in range(len(liste)):
        modalités, effectifs = np.unique(liste[x], return_counts = True)
        taille = np.size(liste[x])
        frequences.append(np.array([e/taille for e in effectifs]).tolist())
    return frequences


async def frequences_cumulees (liste) :
    frequences_cumulees = []
    for x in range(len(liste)):
        modalités, effectifs = np.unique(liste[x], return_counts = True)
        taille = np.size(liste[x])
        frequences = np.array([e/taille for e in effectifs])
        frequences_cumulees.append(np.cumsum(frequences).tolist())
    return frequences_cumulees



import numpy as np

async def interet_personnes(listeFavoris, listePrix, listePrixMagasin):
    interets = []
    
    for i in range(len(listeFavoris)):
        if not listePrix[i]:  
            interets.append(0)
            continue
        
        total_favoris = np.sum(listeFavoris[i]) or 1  

        scores_interet = []
        for j in range(len(listePrix[i])): 
            prix_vente = listePrix[i][j]
            prix_magasin = listePrixMagasin[j] if j < len(listePrixMagasin) else prix_vente

            favoris = listeFavoris[i][j]
            ponderation = np.log1p(favoris) / np.log1p(total_favoris)
            difference_prix = max((prix_magasin - prix_vente) / prix_magasin, -1)

            interet = ponderation * difference_prix * 100  
            scores_interet.append(interet)

        score_total = np.sum(scores_interet)  
        score_normalise = max(min(score_total, 100), -100)  
        interets.append(score_normalise)
    
    return interets




async def main():
    import numpy as np
    import matplotlib.pyplot as plt

    import matplotlib.pyplot as plt
    import numpy as np

    async def afficher_graphique(listeFavoris, listePrix, listePrixMagasin):
        # Création de la figure avec 3 sous-graphes
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))

        # Liste pour stocker les données traitées
        for i in range(3):
            # Sélection des données à afficher
            prix_vente = listePrix[i]
            favoris = listeFavoris[i]

            # Calcul de la médiane et de la moyenne
            mediane = np.median(prix_vente)
            moyenne = np.mean(prix_vente)
            
            # Calcul des quartiles
            q1 = np.percentile(prix_vente, 25)  # 1er quartile
            q2 = mediane  # Q2 est la médiane
            q3 = np.percentile(prix_vente, 75)  # 3e quartile

            # Création du graphique pour chaque niche
            axs[i].plot(prix_vente, label=f'Niche {i+1}', color='b', marker='', linestyle='-', alpha=0.7)
            axs[i].axhline(moyenne, color='g', linestyle='--', label=f'Moyenne: {moyenne:.2f}')
            axs[i].axhline(mediane, color='r', linestyle='-', label=f'Médiane: {mediane:.2f}')
            axs[i].axhline(q1, color='orange', linestyle=':', label=f'Q1: {q1:.2f}')
            axs[i].axhline(q3, color='purple', linestyle=':', label=f'Q3: {q3:.2f}')

            # Titres et labels
            axs[i].set_title(f'Graphique Niche {i+1}')
            axs[i].set_xlabel('Index des produits')
            axs[i].set_ylabel('Prix')
            axs[i].legend()

            # Enregistrement de chaque graphique séparément
            axs[i].figure.savefig(f'graphique_niche_{i+1}.png')

        # Ajuster les marges et afficher tous les graphiques
        plt.tight_layout()
        plt.show()





    jsons = await chargerJson()
    prix_liste = await chargerPrix(jsons)
    favoris_liste = await chargerFavoris(jsons)
    await afficher_graphique(favoris_liste, prix_liste, listePrixMagasin)

    # print(len(prix_liste[0]), len(prix_liste[1]), len(prix_liste[2]))
    stats = {
        "prix": {
            "max" : [
                max(prix_liste[0]),
                max(prix_liste[1]),
                max(prix_liste[2])
            ],
            "min" : [
                min(prix_liste[0]),
                min(prix_liste[1]),
                min(prix_liste[2])
            ],
            "moyenne": await moyenne(prix_liste),
            "mediane": await mediane(prix_liste),
            "ecart_type": await ecart_type(prix_liste),
            "quartiles": dict(zip(["Q1", "Q2", "Q3"], await quartiles(prix_liste))),
            "intéret" : await interet_personnes(favoris_liste, prix_liste, listePrixMagasin),
            "effectifs": await effectifs(prix_liste),
            "frequences": await frequences(prix_liste),
        },
        "favoris": {
            "moyenne": await moyenne(favoris_liste),
            "mediane": await mediane(favoris_liste),
            "ecart_type": await ecart_type(favoris_liste),
            "quartiles": dict(zip(["Q1", "Q2", "Q3"], await quartiles(favoris_liste))),
            "effectifs": await effectifs(favoris_liste),
            "frequences": await frequences(favoris_liste),
        }
    }

    with open("resultat.json", "w", encoding="utf8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)
    print("Les statistiques ont été enregistrées dans resultat.json")

asyncio.run(main())
