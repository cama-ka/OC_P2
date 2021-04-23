import os
import requests
from bs4 import BeautifulSoup
import csv
from scrap_one import book_one
from scrap_one import ecriture_info


def creation_repertoires():
    ''' Creating two folders : books and images '''
    try:
        os.mkdir('books/')
        os.mkdir('images/')
    except OSError:
        pass
    else:
        pass
        
                    
def pagination(lien, cat, URL):
    ''' We have to go into every pages of a category '''
    lien = lien.replace("index.html", "page-1.html")
    r = requests.get(lien)
    if r.ok:
        i = 1
        while r.ok:
            lien_livre(lien, cat, URL)
            i += 1
            lien = lien.replace("page-" + str(i - 1) + ".html", "page-" + str(i) + ".html")
            r = requests.get(lien)   
    else:
        lien = lien.replace("page-1.html", "index.html")
        r = requests.get(lien)
        if r.ok:
            lien_livre(lien, cat, URL)
                    

def lien_livre(lien, cat, URL):
    ''' Go to url of the category. '''
    r = requests.get(lien)
    if r.ok: 
        lien = BeautifulSoup(r.content, "lxml")
        for li in lien.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
            for h3 in li.find_all('h3'):
                lien_livre = h3.a.attrs['href']
                url_du_livre = URL.replace('index.html','') + \
                    lien_livre.replace('../../../','catalogue/').replace('../../','catalogue/')
                print(url_du_livre)
                book_one(url_du_livre, cat)
                ecriture_info(url_du_livre, cat)
                   
    
def main(URL):
    """ The main function it's gonna find links for each categorys,\
        creat csv files and activate the others function"""
    creation_repertoires()

    response = requests.get(URL)
    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        for ultag in soup.find_all('ul', {'class': 'nav nav-list'}):
            ultagul = ultag.find('ul')
            for litag in ultagul.find_all('li'):
                link_category = litag.a.attrs['href']
                cat = link_category.replace("catalogue/category/books/","").replace('/index.html','')
                lien = "https://books.toscrape.com/" + link_category
                with open('books/' + cat + '.csv', 'w', encoding='utf-8-sig') as file:
                    csv_writer = csv.writer(file, delimiter=';')
                    file.write('product_page_url;universal_product_code;title;price_including_tax;'
                    'price_excluding_tax;number_available;product_description;category;'
                    'review_rating;image_url;image_path;\n')
                    print(f"{cat} est en cours de téléchargement")
                pagination(lien, cat, URL)
                       
    
if __name__ == "__main__":
    main("https://books.toscrape.com/index.html")