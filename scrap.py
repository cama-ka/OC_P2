import os
import requests
from bs4 import BeautifulSoup
from scrap_one import book_one


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
    # If http:// xxx.page-1.html exist, we find her and replace the 1 and go for the second page.
        i = 1
        while r.ok:
            lien_livre(lien, cat, URL)
            # replace the number of the page until the response is not ok
            i += 1
            lien = lien.replace("page-" + str(i - 1) + ".html", "page-" + str(i) + ".html")
            r = requests.get(lien)   
    else:
    # If the url is not ok, don't change and execute lien_livre function
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
                    # Find the link of a book and execute the info_livre function
                book_one(url_du_livre, cat)
                    
    
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
                    file.write('product_page_url;universal_product_code;title;price_including_tax;'
                    'price_excluding_tax;number_available;product_description;category;'
                    'review_rating;image_url;image_path;\n')
                pagination(lien, cat, URL)
                        
    
if __name__ == "__main__":
    main("https://books.toscrape.com/index.html")