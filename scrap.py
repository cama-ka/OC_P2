import os
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/index.html"
liste_des_liens_categories = []
liste_cat_2 = []

def creation_repertoires():
    # Je cree deux repertoires : un pour les images et un pour les csv.
    try:
        os.mkdir('books/')
    except OSError:
        pass
    else:
        pass
                    
def pagination():
    # Il faut aller sur chaque page de chaque catégorie.
    for lien in liste_des_liens_categories:
        lien = lien.replace("index.html", "page-1.html")
        r = requests.get(lien)
        # print(lien)
        if r.ok:
            i = 1
            while r.ok:
                i += 1
                lien = lien.replace("page-" + str(i - 1) + ".html", "page-" + str(i) + ".html")
                r = requests.get(lien) # Indispensable pour chercher une nouvelle categorie sinon pagine indéfiniment sur "mystery"
                if r.ok:
                    liste_cat_2.append(lien)
                    
        else:
            lien = lien.replace("page-1.html", "index.html")
            # print( "no second page " + lien)
        

def lien_livre():
    for lien in liste_cat_2:
        r = requests.get(lien)
        if r.ok: 
            lien = BeautifulSoup(r.content,features='html.parser')
            for li in lien.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
                for h3 in li.find_all('h3'):
                    lien_livre = h3.a.attrs['href']
                    url_du_livre = URL.replace('index.html','') + lien_livre.replace('../../../','catalogue/').replace('../../','catalogue/') #recherche de l'url du livre


    

# def info_livre(url_du_livre,cat):
    # Pour chaque livre, on récupère les infos. On les retranscris sur les fichiers csv crees au prealable.
    # response = requests.get(urlDuLivre)
    # if response.ok:
        # with open('books/' + cat.replace('https://books.toscrape.com/catalogue/category/books','').replace('/index.html','') + '.csv','a', encoding='utf-8') as file: #j'ouvre le fichier books + cat qui changera a chaque quoi + le type de fichier, en mode append
            # soup = BeautifulSoup(response.content, features="html.parser")
            # tds = soup.find_all('td')
            # universalProductCode = tds[0].text.replace(',', '').replace(';', '')
            # priceIncludingTax = tds[3].text.replace(',', '').replace(';', '')
            # priceExcludingTax = tds[2].text.replace(',', '').replace(';', '')
            # numberAvailable = tds[5].text.replace(',', '').replace(';', '')
            # reviewRating = tds[6].text.replace(',', '').replace(';', '')
            # title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text.replace(',', '').replace(';', '')
            # productDescription = soup.find('article', {'class': 'product_page'}).find_all('p')[3].text.replace(',', '').replace(';', '')
            # category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].text.replace(',', '').replace(';', '')
            # imageUrl = soup.find('div', {'class': 'item active'}).find('img').attrs['src'].replace('../..', 'http://books.toscrape.com')
            # file.write(urlDuLivre + ';' + universalProductCode + ';' + title + ';' + priceIncludingTax + ';' + priceExcludingTax + ';' + numberAvailable + ';' + productDescription + ';' + category + ';' + reviewRating + ';' + imageUrl + '\n')


def main():
    """ Je cree la fonction principale.\
        Elle va activer les autres fonctions et remplir les fichiers csv."""
    creation_repertoires()

    # Il faut trouver les liens de chaque categorie.
    response = requests.get(URL)
    if response.ok:
        soup = BeautifulSoup(response.content, features="html.parser")
        for ultag in soup.find_all('ul', {'class': 'nav nav-list'}):
                for litag in ultag.find_all('li'):
                    linkCategory = litag.a.attrs['href']
                    liste_des_liens_categories.append('https://books.toscrape.com/' + linkCategory)
                    cat = litag.a.text.replace(" ","").replace('/n','').replace('\n','')
                    print(cat)
    liste_des_liens_categories.pop(0) # suppression du premier lien car books/ contient tous les livres.
    # ATTENTION a placer le print au bon endroit, sinon bug !!!
    pagination()
    
    liste_cat_2.extend(liste_des_liens_categories)
    lien_livre()
    print(liste_cat_2)



if __name__ == "__main__":
    main()