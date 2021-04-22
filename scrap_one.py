import os
import requests
from bs4 import BeautifulSoup
import csv

def creation_repertoires():
    # Creating folder
    try:
        os.mkdir('books/')
        os.mkdir('images/')
    except OSError:
        pass
    else:
        pass



def book_one(url_du_livre, cat):
    response = requests.get(url_du_livre)
    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        tds = soup.find_all('td')
        universal_product_code = tds[0].text.replace(',', '').replace(';', '')
        price_including_tax = tds[3].text.replace(',', '').replace(';', '')
        price_excluding_tax = tds[2].text.replace(',', '').replace(';', '')
        number_available = tds[5].text.replace(',', '').replace(';', '')
        review_rating = review_rating_f(url_du_livre)
        title = soup.find('div', {'class': 'col-sm-6 product_main'}).\
            find('h1').text.replace(',', '').replace(';', '')
        product_description = soup.find('article', {'class': 'product_page'}).\
            find_all('p')[3].text.replace(',', '').replace(';', '')
        category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].\
            text.replace(',', '').replace(';', '')
        image_url = soup.find('div', {'class': 'item active'}).find('img').\
            attrs['src'].replace('../..', 'http://books.toscrape.com')
        image_path = image_path_f(universal_product_code)
        image_download(image_url, universal_product_code)
        infos = f"{url_du_livre};{universal_product_code};{title};{price_including_tax};{price_excluding_tax};{number_available};{product_description};{category};{review_rating};{image_url};{image_path}"
                       
        return infos
    

def image_path_f(universal_product_code):
    path = "images/" + universal_product_code + ".jpg"
    if os.path.exists:
        image_path = path
    else : 
        image_path = "doesn't exist"
    
    return image_path
    
        
def review_rating_f(url_du_livre):
    response = requests.get(url_du_livre)
    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
    dic = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    for clef in dic.keys(): 
        if clef == review_rating:
            review_rating = str(dic[clef])
            return review_rating
        else:
            pass
            
        
def on_y_vas(cat):
    info = book_one("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", cat)
    with open('books/' + cat + '.csv', 'a', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file, delimiter=';')
        file.write(info)
    
    
def image_download(image_url, product_code):
# Uploading images of each book in the folder we created before.
    response = requests.get(image_url)
    with open('images/' + product_code + '.jpg' , "wb") as file:
        file.write(response.content)
    
    
def main(cat):
    """ The main function it's gonna find links for each categorys,\
        creat csv files and activate the others function"""
    creation_repertoires()
    
    with open('books/' + cat + '.csv', 'w', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file, delimiter=';')
        file.write('product_page_url;universal_product_code;title;price_including_tax;'
        'price_excluding_tax;number_available;product_description;category;'
        'review_rating;image_url;image_path;\n')
        print(f"{cat} est en cours de téléchargement")
                                    
    on_y_vas(cat)

    
if __name__ == "__main__":
    main("Un_livre")