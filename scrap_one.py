import os
import requests
from bs4 import BeautifulSoup
import csv

def creation_repertoires(dossier):
    """ creating directories """
    try:
        os.mkdir(dossier)
        
    except OSError:
        pass
    else:
        pass


def book_one(url_du_livre, cat):
    """ taking informations from each book """
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
        infos = [url_du_livre,universal_product_code,title,\
        price_including_tax,price_excluding_tax,number_available,\
        product_description,category,review_rating,image_url,image_path]
        return infos
    else:
        print("The page cannot be find.")
    

def image_path_f(universal_product_code):
    """ find the image relative path """
    path = f"images/{ universal_product_code }.jpg"
    if os.path.exists:
        image_path = path
    else : 
        image_path = f"Doesn't exist"
    
    return image_path
    
        
def review_rating_f(url_du_livre):
    """  take the review_rating for each book """
    response = requests.get(url_du_livre)
    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
    else:
        print("The page cannot be find.")
    dic = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    if review_rating in dic:
        return dic[review_rating]
    else:
            pass
            
        
def ecriture_info(url_du_livre, cat):
    """ taking information's book to write them in a csv file """
    info = book_one(url_du_livre, cat)
    with open(f"books/ {cat} .csv", 'a', encoding='utf-8-sig', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(info)
    
    
def image_download(image_url, product_code):
    """ Upload images """
    response = requests.get(image_url)
    with open(f"images/ {product_code} .jpg" , "wb") as file:
        file.write(response.content)
        
    
def main(cat):
    """ create csv files and activate the others function """
    creation_repertoires('books/')
    creation_repertoires('images/')
    
    with open(f"books/ {cat} .csv", 'w', encoding='utf-8-sig', newline="") as csvfile:
        fieldnames = ["product_page_url","universal_product_code","title","price_including_tax",\
                "price_excluding_tax","number_available","product_description","category",\
                "review_rating","image_url","image_path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        print(f"{cat} est en cours de t??l??chargement")
        
    ecriture_info("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", cat)

    
if __name__ == "__main__":
    main("Un_livre")