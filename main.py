import requests#funciona con HTTP/1.1
import pandas as pd
import re
from bs4 import BeautifulSoup
from colorama import Fore #para añadir colores a los comentarios 
import time


page_website= 'https://quotes.toscrape.com/page/'
about_website= 'https://quotes.toscrape.com/author/{}'

#def about_scraping():


def quote_scraping():
    quote_data=[]
    page_number=1
    while True: #bucle para actualizar la pagina web si se añade contenido en base a si aumenta el número de páginas en la web
        website = f'{page_website}{page_number}'#formato
        print(f"{Fore.GREEN}Descargando página {page_number}: {website}{Fore.RESET}")
        
        try:
            contenido = requests.get(website)
            contenido.raise_for_status()  
        except requests.RequestException as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")
            break

        soup = BeautifulSoup(contenido.text, 'html.parser')
        data=soup.findAll('div',class_='quote')  

        if not data:
            print(f"{Fore.YELLOW}Datos no encontrados en página {page_number}. Termina el scrape.{Fore.RESET}")
            break

        for div in data:
            cita=div.find('span',class_='text').text.strip()
            autor=div.find('small',class_='author').text.strip()
            tags = []
            for tag in div.findAll('a', class_='tag'):
                tags.append(tag.text)

            diccionario={'Cita':cita,'Autor':autor,'Tag':', '.join(tags)}#','.join(tags) para unir todos los tagas en un str y separarlos con ,
            quote_data.append(diccionario)            
            #print(quote_data)


        page_number +=1 #page_number = page_number + 1
        time.sleep(2)#tiempo que pasa entre una vuelta y otra que da el while

    df = pd.DataFrame(quote_data)
    #df=df[['Cita':'CITA','Autor':'AUTOR','Tag':'TAGS']]
    print(df)
        
quote_scraping()
    
"""while True:
        website = page_website.format(page_number)
        print(f'Scrapeando la página: {website}')
        web_scraping(website)
        page_number +=1 #page_number = page_number + 1
        if not website:
            print(f"No quotes found on page {page_number}. Ending scrape.")
        break"""
        

"""for page_number in range(1, 11):
    website = page_website.format(page_number)
    print(f'Scrapeando la página: {website}')
    web_scraping(website)"""    




#about=soup.find_all('div',class_='author_details')
"""def about_author(website):
    contenido= requests.get(website)
    soup = BeautifulSoup(contenido.text, 'lxml')
    about=soup.find_all('div',class_='quote')


#about=soup.find_all('a',class_='href')
#print(about)"""