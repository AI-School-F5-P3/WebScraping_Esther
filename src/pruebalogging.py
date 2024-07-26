import logging.config
import requests#funciona con HTTP/1.1
import pandas as pd
import re #expresiones regulares que permiten reemplazar múltiples caracteres a la vez
from bs4 import BeautifulSoup
from colorama import Fore #para añadir colores a los comentarios 
import time
import logging
'''Para testear que ciertos bloques de código se ejecuten o no. 5 tipos de mensaje:
Debug=10(testear cierta parte de nuestro código),
Info=20(se encuentra en el flujo normal de la app)
Warning=30(alerta)
Error=40(mensaje de errores)
Critical=50(alerta de que el programa ya no puede continuar)'''

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename= 'WebScraping_Esther/log/scraping.log',
                    filemode='a')

page_website= 'https://quotes.toscrape.com/page/'
about_website= 'https://quotes.toscrape.com/author/'

'''def about_scraping():
    about_author=[]
    #author=re.sub(r'[ ,.]', '-',autor)
    author_website=f'{about_website}{author}'
    contenido_author = requests.get(author_website)
    soup = BeautifulSoup(contenido_author.text, 'html.parser')
    about=soup.find('div',class_='author_details')
    diccionario_about={'About': about}
    about_author.append(diccionario_about)
    print(about_author)
about_scraping()'''

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
            logging.error(f"{Fore.RED}Error: {e}{Fore.RESET}")
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
            #logging.info(quote_data)
            #about_scraping(autor)


        page_number +=1 #page_number = page_number + 1
        time.sleep(2)#tiempo que pasa entre una vuelta y otra que da el while

    df = pd.DataFrame(quote_data)

    logging.info(df)
        
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