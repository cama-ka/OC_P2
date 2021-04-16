import os
import requests
from bs4 import BeautifulSoup


url_du_livre = "https://books.toscrape.com/catalogue/olio_984/index.html"

def creation_repertoires():
    # Creating folder
    try:
        os.mkdir('one_book/')
        os.mkdir('image/')
    except OSError:
        pass
    else:
        pass

def book_one():
    response = requests.get(url_du_livre)
    if response.ok:
        print(url_du_livre)
        with open('one_book/' + 'olio' + '.csv', 'a', encoding='utf-8-sig') as file:
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
            path = "image/" + universal_product_code + ".jpg"
            if os.path.exists:
                image_path = path
            else : 
                image_path = "doesn't exist"
            print(image_path)
            file.write(url_du_livre + ';' + universal_product_code + ';' + title +\
                ';' + price_including_tax + ';' + price_excluding_tax + ';' + number_available +\
                ';' + product_description + ';' + category + ';' + review_rating + ';' + image_url + ';' + image_path +'\n')
    
    
def image_download(image_url, product_code):
# Uploading images of each book in the folder we created before.
	response = requests.get(image_url)
	file = open('image/' + product_code + '.jpg' , "wb")
	file.write(response.content)
	file.close()
    
    
def main():
    """ The main function it's gonna find links for each categorys,\
        creat csv files and activate the others function"""
    creation_repertoires()
    
    with open('one_book/' + 'olio' + '.csv', 'w', encoding='utf-8-sig') as file:
        file.write('product_page_url;universal_product_code;title;price_including_tax;'
        'price_excluding_tax;number_available;product_description;category;'
        'review_rating;image_url;image_path;\n')
        
    book_one()
                        
    
if __name__ == "__main__":
    main()