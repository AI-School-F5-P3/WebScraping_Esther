# Base URL for pages
import requests#funciona con HTTP/1.1
import pandas as pd
import re
from bs4 import BeautifulSoup
from colorama import Fore #para añadir colores a los comentarios 
import time

page_website = 'https://quotes.toscrape.com/page/'

def web_scraping():
    quote_data = []
    page_number = 1
    while True:
        website = f'{page_website}{page_number}'
        print(f"{Fore.GREEN}Downloading page {page_number}: {website}{Fore.RESET}")
        
        # Make the request
        try:
            response = requests.get(website)
            response.raise_for_status()  # Check for HTTP request errors
        except requests.RequestException as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")
            break
        
        # Parse the content
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes_divs = soup.findAll('div', class_='quote')
        
        if not quotes_divs:
            print(f"{Fore.YELLOW}No more data found. Exiting.{Fore.RESET}")
            break
        
        for div in quotes_divs:
            cita = div.find('span', class_='text').text.strip()
            autor = div.find('small', class_='author').text.strip()
            tags = [tag.text for tag in div.findAll('a', class_='tag')]

            diccionario = {'Cita': cita, 'Autor': autor, 'Tags': ', '.join(tags)}
            quote_data.append(diccionario)
        
        page_number += 1
    
    df = pd.DataFrame(quote_data)
    print(df)


web_scraping()