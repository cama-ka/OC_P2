# Scrapper les informations du site book.toscrape.

**Pour utiliser cette application suivez la procédure ci-dessous.**

*Cette procédure a été conçue pour l'OS Windows 10. Certaines commandes peuvent varier selon votre OS.*

### Pré-requis:
Installez Python 3 : [https://www.python.org/downloads/](https://wprock.fr/blog/)https://www.python.org/downloads/

#### Télécharger le programme via GitHub avec la commande ci-dessous ou en téléchargeant l'archive: 

	git clone https://github.com/cama-ka/OC_P2.git

1. Se rendre dans le répertoire du projet dans un terminal:
	- cd "répertoire/du/projet"

2. Créer l'environnement virtuel:
	- python3 -m venv env

3. Activer l'environnement virtuel:
	- env\Scripts\Activate.bat

4. Installer les modules via la commande:
	- pip install -r requirements.txt


## Pour lancer le programme traitant d'un seul livre :
* python scrap_one.py

##### Informations scrap_one.py
- Les informations du livre seront contenues dans un fichier .CSV et se trouve dans le répertoire /books/.
- L'image du livre sera télécharger dans le répertoir /images/.

#### Pour lancer le programme traitant tous les livres du site :
* python scrap.py

##### Informations scrap.py
- Le script scrap.py est lié au script scrap_one.py

- Chaque catégorie correspond à un fichier .CSV et se trouve dans le répertoire /books/.

- Chaque ligne dans le fichier .CSV correspond à un livre (sauf l'entête).

- Toutes les images sont enregistrées dans le répertoire: /images/.

- Le séparateur utilisé dans le fichier .CSV est la virgule (,).

- Les répertoires (/books/ et /images/) et les fichiers .CSV sont créés automatiquement au lancement du programme.

- Les images sont nommées par le numéro de produit unique de chaque livre.