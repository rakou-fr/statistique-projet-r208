import asyncio
import matplotlib.pyplot as plt
import numpy as np
import os
import json


async def charger_json():
    lesJsons = ["./SRC/JSON/RL.json", "./SRC/JSON/Corteiz.json", "./SRC/JSON/H&M.json"]
    retourJson = []
    try:
        for x in range(len(lesJsons)):
            with open(lesJsons[x], "r", encoding="utf8") as fichier:
                retourJson.append(json.load(fichier))
    except FileNotFoundError:
        print("")
    return retourJson

async def moyenne (Liste) :
    return np.mean(Liste)

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




print(asyncio.run(charger_json()))

def plot_with_custom_theme(theme_path, data):
    """
    Affiche un graphique avec Matplotlib en appliquant un thème personnalisé.
    
    :param theme_path: Chemin vers le fichier du thème Matplotlib (.mplstyle)
    :param data: Données sous forme de dictionnaire { 'x': [...], 'y': [...] }
    """
    if not os.path.exists(theme_path):
        print(f"Le fichier de thème {theme_path} n'existe pas.")
        return

    plt.style.use(theme_path)
    
    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'], label='Données')
    
    ax.set_xlabel('Axe X')
    ax.set_ylabel('Axe Y')
    ax.set_title('Graphique avec Thème Personnalisé')
    ax.legend()

    plt.show()

data_example = {
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 25, 30, 40]
}

theme_file = "./SRC/rose-pine-matplotlib/themes/rose-pine.mplstyle"
# plot_with_custom_theme(theme_file, data_example)