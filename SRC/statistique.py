import asyncio
#asyncio.run(funct(para))

async def exemple(para : str):
    '''
    entre : 
    sortie :
    texte récap
    '''
    code = 0
    return code

    
    
import matplotlib.pyplot as plt
import os

def plot_with_custom_theme(theme_path, data):
    """
    Affiche un graphique avec Matplotlib en appliquant un thème personnalisé.
    
    :param theme_path: Chemin vers le fichier du thème Matplotlib (.mplstyle)
    :param data: Données sous forme de dictionnaire { 'x': [...], 'y': [...] }
    """
    if not os.path.exists(theme_path):
        print(f"Le fichier de thème {theme_path} n'existe pas.")
        return
    
    # Charger le thème
    plt.style.use(theme_path)
    
    # Création du graphique
    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'], label='Données')
    
    ax.set_xlabel('Axe X')
    ax.set_ylabel('Axe Y')
    ax.set_title('Graphique avec Thème Personnalisé')
    ax.legend()
    
    # Affichage du graphique
    plt.show()

# Exemple d'utilisation
data_example = {
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 25, 30, 40]
}

theme_file = "./SRC/rose-pine-matplotlib/themes/rose-pine.mplstyle"
plot_with_custom_theme(theme_file, data_example)