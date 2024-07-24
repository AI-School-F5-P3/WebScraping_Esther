import requests#funciona con HTTP/1.1
import pandas as pd
import re
from bs4 import BeautifulSoup
from colorama import Fore
#Hay 10 páginas en total que scrapear

website='https://quotes.toscrape.com/'
page_website= 'https://quotes.toscrape.com/page/{}'

def web_scraping(website):
    contenido= requests.get(website)
    soup = BeautifulSoup(contenido.text, 'lxml')
    cita=soup.find_all('span',class_='text')
    autor=soup.find_all('small',class_='author')
    about=soup.find_all('div',class_='author_details')
    tag=soup.find_all('meta',class_='keywords')
    print (cita)
    print(autor)    
    print(tag)

for page_number in range(1, 11):
    website = page_website.format(page_number)
    print(f'Scrapeando la página: {website}')
    web_scraping(website)


"""def about_author(website):
    contenido= requests.get(website)
    soup = BeautifulSoup(contenido.text, 'lxml')
    about=soup.find_all('div',class_='quote')


#about=soup.find_all('a',class_='href')
#print(about)"""