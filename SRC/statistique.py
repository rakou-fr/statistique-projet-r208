import asyncio
import matplotlib.pyplot as plt
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