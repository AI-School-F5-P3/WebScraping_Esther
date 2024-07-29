import requests#funciona con HTTP/1.1
import pandas as pd
from bs4 import BeautifulSoup
from colorama import Fore #para añadir colores a los comentarios 
import time
from unidecode import unidecode #para estandarizar el lenguaje(limpiamos los acentos)
from dotenv import load_dotenv #Para conectar con la db, y nos traemos la información de las variables creadas en el archivo .env
import os #librería para interactuar con otros archivos
from sqlalchemy import create_engine #Comunicación con db.
import psycopg2 #Conectar con PostgreSQL
import logging #Para los logs
import pytest #Test unitarios

'''Para testear que ciertos bloques de código se ejecuten o no. 5 tipos de mensaje:
Debug=10(testear cierta parte de nuestro código),
Info=20(se encuentra en el flujo normal de la app)
Warning=30(alerta)
Error=40(mensaje de errores)
Critical=50(alerta de que el programa ya no puede continuar)'''

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename= 'WebScraping_Esther/log/scraping.log',
                    filemode='a',
                    encoding='utf-8' )

load_dotenv() #Para conectar con la db, y nos traemos la información de las variables creadas en el archivo .env
USER = os.getenv('USER')
PWD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

try:
    conexion = psycopg2.connect(
        dbname=DATABASE,
        user=USER,
        password=PWD,
        host=HOST,
        port=PORT
    )
    print(f'{Fore.BLUE}Conexión exitosa a la base de datos: {DATABASE}!{Fore.RESET}')
    logging.info(f'{Fore.BLUE}Conexión exitosa a la base de datos: {DATABASE}!{Fore.RESET}')
    conexion.close()
except Exception as e:
    logging.error(f"Conexión fallida: {e}")


connection_string = f'postgresql://{USER}:{PWD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(connection_string) #motor necesario para asegurar la comunicación entre la app y la db
table_name= 'XYZCorp_Datos'


page_website= 'https://quotes.toscrape.com/page/'
about_website= 'https://quotes.toscrape.com/author/'

def about_scraping(autor_limpieza):
    author_website=f'{about_website}{autor_limpieza}'
    print(f"{Fore.GREEN}Descargando autor {autor_limpieza}: {author_website}{Fore.RESET}")
    logging.info(f"{Fore.GREEN}Descargando autor {autor_limpieza}: {author_website}{Fore.RESET}")
    contenido_author = requests.get(author_website)
    if contenido_author.status_code == 404:
        logging.error(f"Página para {autor_limpieza} no encontrada (404). Termina scrape.")
        return None  
    elif contenido_author.status_code != 200:
        logging.error(f"Error en la página para {autor_limpieza}. Status code: {contenido_author.status_code}. Termina scrape.")
        return None
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
        logging.info(f"{Fore.MAGENTA}Descargando página {page_number}: {website}{Fore.RESET}")
        
        try:
            contenido = requests.get(website)
            contenido.raise_for_status() #Estado de la respuesta  
        except requests.RequestException as e:
            logging.error(f"{Fore.RED}Error: {e}{Fore.RESET}")
            break

        soup = BeautifulSoup(contenido.text, 'html.parser')
        data=soup.findAll('div',class_='quote')  

        if not data:
            print(f"{Fore.YELLOW}Datos no encontrados en página {page_number}. Termina el scrape.{Fore.RESET}")
            logging.info(f"{Fore.YELLOW}Datos no encontrados en página {page_number}. Termina el scrape.{Fore.RESET}")
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
                'Tag':', '.join(tags), #','.join(tags) para unir todos los tags en un str y separarlos con ,
                'Fecha_Nacimiento':autor_info['Fecha_Nacimiento'],
                'Lugar_nacimiento':autor_info['Lugar_nacimiento'],
                'Descripcion':autor_info['Descripcion']
                }
            quote_data.append(diccionario)            
            

        page_number +=1 #page_number = page_number + 1
        time.sleep(2)#tiempo que pasa entre una vuelta y otra que da el while

    df = pd.DataFrame(quote_data)
    return df


if __name__ == "__main__":
    df_final = quote_scraping()
    # Enviar el DataFrame a la base de datos
    try:
        df_final.to_sql(table_name, engine, if_exists='replace', index=False) #
        print(f"{Fore.BLUE}DataFrame enviado a la tabla {table_name} en la base de datos {DATABASE}{Fore.RESET}")
        logging.info(f"{Fore.BLUE}DataFrame enviado a la tabla {table_name} en la base de datos {DATABASE}{Fore.RESET}")
    except Exception as e:
        logging.error(f"{Fore.RED}Error al enviar el DataFrame a la base de datos: {e}{Fore.RESET}")

logging.info(df_final)