import os
import requests
from bs4 import BeautifulSoup


URL = "https://books.toscrape.com/index.html"

def creation_repertoires():
    # Je cree deux repertoires : un pour les images et un pour les csv.
    try:
        os.mkdir('books/')
        os.mkdir('images/')
    except OSError:
        pass
    else:
        pass
        
                    
def pagination(lien, cat):
        lien = lien.replace("index.html", "page-1.html")
        r = requests.get(lien)
        # print(lien)
        if r.ok:
            i = 1
            while r.ok:
                lien_livre(lien, cat)
                i += 1
                lien = lien.replace("page-" + str(i - 1) + ".html", "page-" + str(i) + ".html")
                r = requests.get(lien) # Indispensable pour chercher une nouvelle categorie sinon pagine indéfiniment sur "mystery"   
        else:
            lien = lien.replace("page-1.html", "index.html")
            r = requests.get(lien)
            if r.ok:
                lien_livre(lien, cat)
                    

def lien_livre(lien, cat):
        r = requests.get(lien)
        if r.ok: 
            lien = BeautifulSoup(r.content, "lxml")
            for li in lien.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
                for h3 in li.find_all('h3'):
                    lien_livre = h3.a.attrs['href']
                    url_du_livre = URL.replace('index.html','') + lien_livre.replace('../../../','catalogue/').replace('../../','catalogue/') #recherche de l'url du livre
                    info_livre(url_du_livre, cat)
                    

def info_livre(url_du_livre, cat):
    # Pour chaque livre, on récupère les infos. On les retranscris sur les fichiers csv crees au prealable.
    print(url_du_livre)
    response = requests.get(url_du_livre)
    if response.ok:
        with open('books/' + cat + '.csv', 'a', encoding='utf-8-sig') as file: #j'ouvre le fichier books + cat qui changera a chaque fois + le type de fichier, en mode append
            soup = BeautifulSoup(response.content, "lxml")
            tds = soup.find_all('td')
            universalProductCode = tds[0].text.replace(',', '').replace(';', '')
            priceIncludingTax = tds[3].text.replace(',', '').replace(';', '')
            priceExcludingTax = tds[2].text.replace(',', '').replace(';', '')
            numberAvailable = tds[5].text.replace(',', '').replace(';', '')
            reviewRating = tds[6].text.replace(',', '').replace(';', '')
            title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text.replace(',', '').replace(';', '')
            productDescription = soup.find('article', {'class': 'product_page'}).find_all('p')[3].text.replace(',', '').replace(';', '')
            category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].text.replace(',', '').replace(';', '')
            imageUrl = soup.find('div', {'class': 'item active'}).find('img').attrs['src'].replace('../..', 'http://books.toscrape.com')
            imageDownload(imageUrl, universalProductCode)
            file.write(url_du_livre + ';' + universalProductCode + ';' + title + ';' + priceIncludingTax + ';' + priceExcludingTax + ';' + numberAvailable + ';' + productDescription + ';' + category + ';' + reviewRating + ';' + imageUrl + '\n')

def imageDownload(imageUrl, productCode):
	response = requests.get(imageUrl)
	file = open('images/' + productCode + '.jpg' , "wb")
	file.write(response.content)
	file.close()
    
    
def main():
    """ Je cree la fonction principale.\
        Elle va activer les autres fonctions et remplir les fichiers csv."""
    creation_repertoires()

    # Il faut trouver les liens de chaque categorie.
    response = requests.get(URL)
    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        for ultag in soup.find_all('ul', {'class': 'nav nav-list'}):
            ultagul = ultag.find('ul')    
            for litag in ultagul.find_all('li'):
                linkCategory = litag.a.attrs['href']
                cat = linkCategory.replace("catalogue/category/books/","").replace('/index.html','')
                lien = "https://books.toscrape.com/" + linkCategory
                with open('books/' + cat + '.csv', 'w', encoding='utf-8-sig') as file:
                    file.write('product_page_url;universal_product_code;title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url;\n')
                pagination(lien, cat)
                        
    
if __name__ == "__main__":
    main()