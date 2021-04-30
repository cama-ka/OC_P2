#Scrapper Bookscrap

Pour utiliser cette application suivez la procédure ci-dessous.

Cette procédure a été conçue pour l'OS Windows 10. Certaines commandes peuvent varier selon votre OS.

Pré-requis:
Installez Python 3 : https://www.python.org/downloads/

Télécharger le programme via GitHub avec la commande ci-dessous ou en téléchargeant l'archive.


git clone https://github.com/cama-ka/OC_P2.git
Se rendre dans le répertoire du projet dans un terminal:
cd "répertoire/du/projet"
Créer l'environnement virtuel:
python3 -m venv env
Activer l'environnement virtuel:
env\Scripts\Activate.bat
installer les modules via la commande:
pip install -r requirements.txt
Lancer le programme:
python app.py

Informations
Chaque catégorie correspond à un fichier .CSV et se trouve dans le répertoire books/

Chaque ligne dans le fichier .CSV correspond à un livre (sauf l'entête).

Toutes les images sont enregistrées dans le répertoire: imgs/

Le séparateur utilisé dans le fichier .CSV est le point-virgule (;).

Les répertoires (../books/ et ../imgs/) et les fichiers .CSV sont créés automatiquement au lancement du programme.

Les images sont nommées par le numéro de produit unique de chaque livre.