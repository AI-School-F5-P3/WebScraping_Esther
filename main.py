import requests#funciona con HTTP/1.1
import pandas as pd
import re
from bs4 import BeautifulSoup
from colorama import Fore

website= 'https://quotes.toscrape.com/'
contenido= requests.get(website)
soup = BeautifulSoup(contenido.text, 'lxml')
frase=soup.find_all('span',class_='text')
autor=soup.find_all('small',class_='author')
about=soup.find_all('a',class_='href')
tag=soup.find_all('meta',class_='keywords')

print (frase)
print(autor)
print(about)
print(tag)



