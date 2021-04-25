import os
import requests
from bs4 import BeautifulSoup
import csv
from scrap_one import book_one
from scrap_one import ecriture_info
from scrap_one import creation_repertoires
        
                    
def pagination(lien, cat, URL):
    ''' Go into every pages of a category '''
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
    else:
        print("The page cannot be find.")
                   
    
def main(URL):
    """ Find links for each categorys, create csv files and activate the others function"""
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
                with open(f"books/ {cat} .csv", 'w', encoding='utf-8-sig', newline="") as csvfile:
                    fieldnames = ["product_page_url","universal_product_code","title","price_including_tax",\
                                "price_excluding_tax","number_available","product_description","category",\
                                "review_rating","image_url","image_path"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                pagination(lien, cat, URL)
    else:
        print("The page cannot be find.")
                       
    
if __name__ == "__main__":
    main("https://books.toscrape.com/index.html")