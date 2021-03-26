import requests
from bs4 import BeautifulSoup
import os

url = "https://books.toscrape.com/"

def main():


	try:
		os.mkdir('books/')
		os.mkdir('imgs/')
	except OSError:
		pass
	else:
		pass

	response = requests.get(url)
	if response.ok:
		soup = BeautifulSoup(response.content, features = "html.parser")
	for ultag in soup.find_all('ul', {'class': 'nav nav-list'}):
		for litag in ultag.find_all('li'):
			linkCategory = litag.a.attrs['href']
			linkCat = [url + linkCategory] #lien pour accéder à la catégorie
			cat = litag.a.text.replace(" ","").replace('/n','').replace('\n','') #récupérer le nom de la catégorie
			for link in range(len(linkCat)):
				print("La catégorie " + cat + " est en cours de chargement.")
				with open('books/' + cat.replace('https://books.toscrape.com/catalogue/category/books','').replace('/index.html','') + '.csv', 'w', encoding='utf-8') as file:
					file.write('product_page_url;universal_product_code;title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n')
					liens_livre(linkCat,cat)
						
							
	# LIENS LIVRES ####################################################################
			
def liens_livre(linkCat,cat):
	for link in linkCat:
		reponseLink = requests.get(link)
		if reponseLink.ok: 
			links = BeautifulSoup(reponseLink.content,features='html.parser')
			for li in links.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
				for h3 in li.find_all('h3'):
					lien = h3.a.attrs['href']
					urlDuLivre = url + lien.replace('../../../','catalogue/').replace('../../','catalogue/') #recherche de l'url du livre
					livre(urlDuLivre,cat)
						
					
	# # ###############################################################################

		
def livre(urlDuLivre,cat):
	response = requests.get(urlDuLivre)
	if response.ok:
		with open('books/' + cat.replace('https://books.toscrape.com/catalogue/category/books','').replace('/index.html','') + '.csv','a', encoding='utf-8') as file: #j'ouvre le fichier books + cat qui changera a chaque quoi + le type de fichier, en mode append
			soup = BeautifulSoup(response.content, features="html.parser")
			tds = soup.findAll('td')
			universalProductCode = tds[0].text.replace(',', '').replace(';', '')
			priceIncludingTax = tds[3].text.replace(',', '').replace(';', '')
			priceExcludingTax = tds[2].text.replace(',', '').replace(';', '')
			numberAvailable = tds[5].text.replace(',', '').replace(';', '')
			reviewRating = tds[6].text.replace(',', '').replace(';', '')
			title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text.replace(',', '').replace(';', '')
			productDescription = soup.find('article', {'class': 'product_page'}).findAll('p')[3].text.replace(',', '').replace(';', '')
			category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text.replace(',', '').replace(';', '')
			imageUrl = soup.find('div', {'class': 'item active'}).find('img').attrs['src'].replace('../..', 'http://books.toscrape.com')
			imageDownload(imageUrl, universalProductCode)
			file.write(urlDuLivre + ';' + universalProductCode + ';' + title + ';' + priceIncludingTax + ';' + priceExcludingTax + ';' + numberAvailable + ';' + productDescription + ';' + category + ';' + reviewRating + ';' + imageUrl + '\n')

	# IMAGES ##########################################################################

def imageDownload(imageUrl, productCode):
	reponse = requests.get(imageUrl)
	file = open('imgs/' + productCode + '.jpg' , "wb")
	file.write(reponse.content)
	file.close()

main()
