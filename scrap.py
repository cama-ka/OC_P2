import os
import requests
from bs4 import BeautifulSoup


URL = "https://books.toscrape.com/index.html"

def creation_repertoires():
    # Creating two folders : books and images
    try:
        os.mkdir('books/')
        os.mkdir('images/')
    except OSError:
        pass
    else:
        pass
        
                    
def pagination(lien, cat):
    # We have to go into every pages of a category
    lien = lien.replace("index.html", "page-1.html")
    r = requests.get(lien)
    if r.ok:
    # If http:// xxx.page-1.html exist, we find her and replace the 1 and go for the second page.
        i = 1
        while r.ok:
        # While the url is ok, got to the function lien_livre
            lien_livre(lien, cat)
            # replace the number of the page until the response is not ok
            i += 1
            lien = lien.replace("page-" + str(i - 1) + ".html", "page-" + str(i) + ".html")
            r = requests.get(lien)   
    else:
    # If the url is not ok, don't change and execute lien_livre function
        lien = lien.replace("page-1.html", "index.html")
        r = requests.get(lien)
        if r.ok:
            lien_livre(lien, cat)
                    

def lien_livre(lien, cat):
    # Go to url of the category.
    r = requests.get(lien)
    if r.ok: 
        lien = BeautifulSoup(r.content, "lxml")
        for li in lien.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
            for h3 in li.find_all('h3'):
                lien_livre = h3.a.attrs['href']
                url_du_livre = URL.replace('index.html','') + \
                    lien_livre.replace('../../../','catalogue/').replace('../../','catalogue/')
                    # Find the link of a book and execute the info_livre function
                info_livre(url_du_livre, cat)
                    

def info_livre(url_du_livre, cat):
    # For each book, take the informations needed and write them in the csv file we made before on the main function.
    print(url_du_livre)
    response = requests.get(url_du_livre)
    if response.ok:
        with open('books/' + cat + '.csv', 'a', encoding='utf-8-sig') as file: 
            #j'ouvre le fichier books + cat qui changera a chaque fois + le type de fichier, en mode append
            soup = BeautifulSoup(response.content, "lxml")
            tds = soup.find_all('td')
            universal_product_code = tds[0].text.replace(',', '').replace(';', '')
            price_including_tax = tds[3].text.replace(',', '').replace(';', '')
            price_excluding_tax = tds[2].text.replace(',', '').replace(';', '')
            number_available = tds[5].text.replace(',', '').replace(';', '')
            p = soup.find_all('p')
            review = str(p[2])
            review_rating = review[0:30]
            if "One" in review_rating:
                review_rating = "1"
            elif "Two" in review_rating:
                review_rating = "2"
            elif "Three" in review_rating:
                review_rating = "3"
            elif "Four" in review_rating:
                review_rating = "4"
            elif "Five" in review_rating:
                review_rating = "5"
            title = soup.find('div', {'class': 'col-sm-6 product_main'}).\
                find('h1').text.replace(',', '').replace(';', '')
            product_description = soup.find('article', {'class': 'product_page'}).\
                find_all('p')[3].text.replace(',', '').replace(';', '')
            category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].\
                text.replace(',', '').replace(';', '')
            image_url = soup.find('div', {'class': 'item active'}).find('img').\
                attrs['src'].replace('../..', 'http://books.toscrape.com')
            image_download(image_url, universal_product_code)
            file.write(url_du_livre + ';' + universal_product_code + ';' + title +\
                ';' + price_including_tax + ';' + price_excluding_tax + ';' + number_available +\
                ';' + product_description + ';' + category + ';' + review_rating + ';' + image_url + '\n')

def image_download(image_url, product_code):
# Uploading images of each book in the folder we created before.
	response = requests.get(image_url)
	file = open('images/' + product_code + '.jpg' , "wb")
	file.write(response.content)
	file.close()
    
    
def main():
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
                    'review_rating;image_url;\n')
                pagination(lien, cat)
                        
    
if __name__ == "__main__":
    main()