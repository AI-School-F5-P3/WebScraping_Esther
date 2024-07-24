import requests#funciona con HTTP/1.1
import pandas as pd
import re
from bs4 import BeautifulSoup
from colorama import Fore
#Hay 10 páginas en total que scrapear

website='https://quotes.toscrape.com/'
page_website= 'https://quotes.toscrape.com/page/{}'
autor_website='https://quotes.toscrape.com/author/{}'
informacion=[]

def web_scraping(website):
    contenido= requests.get(website)
    soup = BeautifulSoup(contenido.text, 'lxml')
    cita=soup.find_all('span',class_='text').get_text(strip=True)
    autor=soup.find_all('small',class_='author').get_text(strip=True)
    about=soup.find_all('div',class_='author_details')  .get_text(strip=True)  
    tag=soup.find_all('meta',class_='keywords').get_text(strip=True)
    author_links = soup.find_all('a', text='(about)').get_text(strip=True)
    
for link in author_links:
    autor_url = autor_website + link['href']
    author_name = link.find_previous('span', class_='nombre-autor')  # Ajustar según la estructura HTML
    about_info = scrape_author_page(autor_url)

    print (cita)
    print(autor)    
    print(tag)

for page_number in range(1, 11):
    website = page_website.format(page_number)
    print(f'Scrapeando la página: {website}')
    web_scraping(website)


def about_author(website):
    contenido= requests.get(website)
    soup = BeautifulSoup(contenido.text, 'lxml')
    about=soup.find_all('div',class_='quote')


#about=soup.find_all('a',class_='href')
#print(about)