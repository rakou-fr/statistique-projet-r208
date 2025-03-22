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
    return np.median(liste)

async def ecart_type (liste) :
    return np.std(liste)

async def quartiles (liste) :
    return np.quantile(liste,0.25, interpolation = 'midpoint'), np.quantile(liste,0.75, interpolation = 'midpoint')

async def effectifs (liste) :
    modalités, effectifs = np.unique(liste, return_counts = True)
    return modalités, effectifs

async def frequences (liste) :
    taille = np.size(liste)
    modalités, effectifs = np.unique(liste, return_counts = True)
    frequences = np.array([e/taille for e in effectifs])
    return frequences

async def frequences_cumulees (liste) :
    modalités, effectifs = np.unique(liste, return_counts = True)
    frequences = np.array([e/taille for e in effectifs])
    taille = np.size(liste)



async def main():
    jsons = await chargerJson()  
    prix_liste = await chargerPrix(jsons)  
    favoris_liste = await chargerFavoris(jsons)  

    print(await moyenne(prix_liste))

asyncio.run(main())
