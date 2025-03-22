import asyncio
import matplotlib.pyplot as plt
import numpy as np
import os
import json

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
                if "favorite_count" in item:
                    favoris.append(int(item["favorite_count"]))
                else:
                    favoris.append(0)
        favoris_par_json.append(favoris)  

    return favoris_par_json

## Statistiques

async def moyenne (Liste) :
    moyenne = []
    for x in range(len(Liste)):
        moyenne.append(np.mean(Liste[x]))
    return moyenne

async def mediane (liste) :
    mediane = []
    for x in range(len(liste)):
        mediane.append(np.median(liste[x]))
    return mediane

async def ecart_type (liste) :
    ecart_type = []
    for x in range(len(liste)):
        ecart_type.append(np.std(liste[x]))
    return ecart_type

async def quartiles (liste) :
    q1 = []
    q3 = []
    for x in range(len(liste)):
        q1.append(np.quantile(liste[x],0.25, method = 'midpoint'))
        q3.append(np.quantile(liste[x],0.75, method = 'midpoint'))
    return q1, q3

async def effectifs (liste) :
    modalités = []
    effectifs = []
    for x in range(len(liste)):
        modalités.append(np.unique(liste[x]))
        effectifs.append(np.size(liste[x]))
    return modalités, effectifs


async def frequences (liste) :
    frequences = []
    for x in range(len(liste)):
        modalités, effectifs = np.unique(liste[x], return_counts = True)
        taille = np.size(liste[x])
        frequences.append(np.array([e/taille for e in effectifs]))
    return frequences

async def frequences_cumulees (liste) :
    frequences_cumulees = []
    for x in range(len(liste)):
        modalités, effectifs = np.unique(liste[x], return_counts = True)
        taille = np.size(liste[x])
        frequences = np.array([e/taille for e in effectifs])
        frequences_cumulees.append(np.cumsum(frequences))



async def main():
    jsons = await chargerJson()  # Charge les JSONs
    prix_liste = await chargerPrix(jsons)  # Charge les prix à partir des JSONs
    favoris_liste = await chargerFavoris(jsons)  # Charge les favoris à partir des JSONs

    # Affichage des résultats statistiques pour les prix
    print("Moyenne des prix:", await moyenne(prix_liste))
    print("Médiane des prix:", await mediane(prix_liste))
    print("Écart-type des prix:", await ecart_type(prix_liste))
    q1, q3 = await quartiles(prix_liste)
    print("1er quartile des prix:", q1)
    print("3ème quartile des prix:", q3)

    # Affichage des résultats statistiques pour les favoris
    print("Moyenne des favoris:", await moyenne(favoris_liste))
    print("Médiane des favoris:", await mediane(favoris_liste))
    print("Écart-type des favoris:", await ecart_type(favoris_liste))
    q1_fav, q3_fav = await quartiles(favoris_liste)
    print("1er quartile des favoris:", q1_fav)
    print("3ème quartile des favoris:", q3_fav)

    # Effectifs et fréquences
    modalités_prix, effectifs_prix = await effectifs(prix_liste)
    print("Modalités des prix:", modalités_prix)
    print("Effectifs des prix:", effectifs_prix)

    fréquences_prix = await frequences(prix_liste)
    print("Fréquences des prix:", fréquences_prix)

    # Fréquences cumulées pour les prix
    frequences_cumulees_prix = await frequences_cumulees(prix_liste)
    print("Fréquences cumulées des prix:", frequences_cumulees_prix)

    # Affichage des résultats pour les favoris
    modalités_fav, effectifs_fav = await effectifs(favoris_liste)
    print("Modalités des favoris:", modalités_fav)
    print("Effectifs des favoris:", effectifs_fav)

    frequences_fav = await frequences(favoris_liste)
    print("Fréquences des favoris:", frequences_fav)

    # Fréquences cumulées pour les favoris
    frequences_cumulees_fav = await frequences_cumulees(favoris_liste)
    print("Fréquences cumulées des favoris:", frequences_cumulees_fav)

asyncio.run(main())
