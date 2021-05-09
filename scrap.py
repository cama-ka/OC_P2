import os
import requests
from bs4 import BeautifulSoup
import csv
from scrap_one import book_one
from scrap_one import ecriture_info
from scrap_one import creation_repertoires
from scrap_one import category

                    
def pagination(lien, cat, URL):
    ''' Go into every pages of a category '''
    lien = lien.replace("index.html", "page-1.html")
    r = requests.get(lien)
    if r.ok:
        i = 1
        while r.ok:
            lien_livre(lien, cat, URL)
            i += 1
            y = 1
            lien = lien.replace(f"page-{i-y}.html", f"page-{i}.html")
            r = requests.get(lien)   
    else:
        lien = lien.replace("page-1.html", "index.html")
        r = requests.get(lien)
        if r.ok:
            lien_livre(lien, cat, URL)
                    

def lien_livre(lien, cat, URL):
    ''' Go to the url of the category. '''
    r = requests.get(lien)
    if r.ok: 
        lien = BeautifulSoup(r.content, "lxml")
        for li in lien.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
            for h3 in li.find_all('h3'):
                lien_livre = h3.a.attrs['href']
                url_du_livre = URL.replace('index.html','') + \
                    lien_livre.replace('../../../','catalogue/').replace('../../','catalogue/')
                nom_du_livre = url_du_livre.replace('https://books.toscrape.com/catalogue/','').replace('/index.html','')
                book_one(url_du_livre, cat)
                ecriture_info(url_du_livre, cat)
    else:
        print("The page cannot be find.")
        pass
                   
    
def main(URL):
    """ Find links for each categories, activate the others function """
    creation_repertoires('books/')
    creation_repertoires('images/')
    
    response = requests.get(URL)
    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        for ultag in soup.find_all('ul', {'class': 'nav nav-list'}):
            ultagul = ultag.find('ul')
            for litag in ultagul.find_all('li'):
                link_category = litag.a.attrs['href']
                cat = link_category.replace("catalogue/category/books/","").replace('/index.html','')
                lien = "https://books.toscrape.com/" + link_category
                category(cat)
                print(f"La catégorie {cat} est en cours d'écriture. Le fichier devrait être visible dans le dossier source.")
                pagination(lien, cat, URL)
    else:
        print("The page cannot be find.")
        pass
                       
    
if __name__ == "__main__":
    main("https://books.toscrape.com/index.html")