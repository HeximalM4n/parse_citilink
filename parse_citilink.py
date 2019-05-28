#!/usr/bin/python

#python 2.7

import requests
from bs4 import BeautifulSoup
from sys import argv

print ('Enter URL to parse Citilink marketplace:')
URL = argv[1]
pathToFile = 'citilink_result.txt'

def GetHtmlSoup(url):
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	return soup

def GetAmountPages(soup):
	a = soup.find('li',class_='last')
	a = a.find('a')
	a = int(a['data-page'])
	return a

curPage = 1
soup = GetHtmlSoup(URL+'/?available=1&p={}'.format(curPage))

# if number of pages 1 
try:
    CountPages = GetAmountPages(soup)
except AttributeError:
    CountPages = 1

file = open(pathToFile,'w')
print ('Parsing..')
count = 0
sumPrice = 0
while curPage <= CountPages:
	_list = soup.find('div',class_ = 'product_category_list')
	for product in _list.find_all('div',class_ = 'js--subcategory-product-item'):
		count += 1
		link = product.find('a').get('href')
		name = product.find('a').get('title').encode('utf-8')
		price = int(product.find('ins', class_ = 'subcategory-product-item__price-num').string.replace(' ',''))
		sumPrice += price
		file.write('\n ********* \n link = {} \n NameProduct = {} \n Value = {}'.format(link, name, price))
	curPage += 1
	url = URL + '/?available=1&p={}'.format(curPage)
	soup = GetHtmlSoup(url)

average_val = sumPrice / count
file.write('\n***************************************************************\n')
file.write('Average price = {} \n Common price = {}\n Count = {}'.format(average_val, sumPrice, count))
file.write('***************************************************************\n')

print ('Operation successfull!')
file.close()
