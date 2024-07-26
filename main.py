import requests#funciona con HTTP/1.1
import pandas as pd
from bs4 import BeautifulSoup
from colorama import Fore #para añadir colores a los comentarios 
import time
from unidecode import unidecode #para estandarizar el lenguaje(limpiamos los acentos)

page_website= 'https://quotes.toscrape.com/page/'
about_website= 'https://quotes.toscrape.com/author/'

def about_scraping(autor_limpieza):
    author_website=f'{about_website}{autor_limpieza}'
    print(f"{Fore.GREEN}Descargando autor {autor_limpieza}: {author_website}{Fore.RESET}")
    contenido_author = requests.get(author_website)
    soup = BeautifulSoup(contenido_author.text, 'html.parser')
    nombre=soup.find('h3', class_= 'author-title').text.strip()
    nacimiento_fecha=soup.find('span', class_= 'author-born-date').text.strip()
    nacimiento_lugar=soup.find('span', class_= 'author-born-location').text.strip()
    descripcion=soup.find('div', class_= 'author-description').text.strip()

    diccionario_about={
        'Nombre': nombre,
        'Fecha_Nacimiento':nacimiento_fecha,
        'Lugar_nacimiento':nacimiento_lugar,
        'Descripcion':descripcion
    }

    return diccionario_about
    

def quote_scraping():
    quote_data=[]
    page_number=1
    while True: #bucle para actualizar la pagina web si se añade contenido en base a si aumenta el número de páginas en la web
        website = f'{page_website}{page_number}'#formato
        print(f"{Fore.MAGENTA}Descargando página {page_number}: {website}{Fore.RESET}")
        
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

            autor_limpieza=unidecode(autor)#estandariza el lenguaje de autor, en este caso quita el acento.
            autor_limpieza=autor_limpieza.replace(' ', '-').replace('.', '-').replace('--', '-').replace("'", '').rstrip('-')
            
            autor_info= about_scraping(autor_limpieza) #llama a la primera función para obtener la info del autor
            
            diccionario={
                'Cita':cita,
                'Autor':autor,
                'Tag':', '.join(tags), #','.join(tags) para unir todos los tagas en un str y separarlos con ,
                'Nombre': autor_info['Nombre'],
                'Fecha_Nacimiento':autor_info['Fecha_Nacimiento'],
                'Lugar_nacimiento':autor_info['Lugar_nacimiento'],
                'Descripcion':autor_info['Descripcion']
                }
            quote_data.append(diccionario)            
            

        page_number +=1 #page_number = page_number + 1
        time.sleep(2)#tiempo que pasa entre una vuelta y otra que da el while

    df = pd.DataFrame(quote_data)
    print(df)
        
quote_scraping()