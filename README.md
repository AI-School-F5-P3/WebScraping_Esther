# WebScraping_Esther
# 🌐 Proyecto Web Scraping

## 📝 Briefing: Proyecto de Web Scraping

### 📋 Planteamiento
La empresa **XYZ Corp** busca una frase que refleje sus valores y misión. Para ello, desarrollaremos un programa en **Python** que realizará **web scraping** para extraer frases de la web [https://quotes.toscrape.com/](https://quotes.toscrape.com/), junto con los autores, tags asociados y la página "about" con información de los autores. Los datos extraídos serán formateados y almacenados adecuadamente.

### 🎯 Objetivos del Proyecto
1. **Acceder a la web**: Obtener frases con información relacionada.
2. **Extraer información**: Utilizar técnicas de web scraping en Python.
3. **Formatear los datos**: Asegurarse de que los datos estén organizados.
4. **Almacenar los datos**: Guardar la información extraída en una base de datos.


### 🛠️ Tecnologías útilizadas
- **Git/GitHub**
- **Python** (bibliotecas: BeautifulSoup,Requests)
- **Herramientas de gestión de proyectos** (Trello)

### 📊 Niveles de Entrega

#### Nivel Esencial
- Script que accede a la web, extrae frases e imprime en consola.
- Limpieza básica de datos extraídos.
- Documentación básica del código y README en GitHub.

### Nivel Medio
- Almacenamiento de los datos extraídos en una base de datos.
- Implementación de un sistema de logs para la trazabilidad del código.

## 📂 Estructura del Proyecto

```plaintext
Proyecto Web Scraping/
├── venv/
├── WebScraping_Esther/
│   ├── log/
│   │   └── scraping.log
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
├── README.md
└── .env

🌟 Descripción Adicional
Creación del Entorno Virtual (venv)
Para crear un entorno virtual en Python y activarlo, se utilizaron los siguientes comandos:

bash

# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual (Windows)
venv\Scripts\activate

# Instalar librerías desde requirements.txt
pip install -r requirements.txt

# Creación del Archivo .env
El archivo .env se utiliza para almacenar información sensible como las credenciales de la base de datos. Para crear el archivo .env, sigue estos pasos:

Crea un archivo llamado .env en la raíz del proyecto.
Añade las siguientes variables con los valores correspondientes:
USER=tu_usuario
PASSWORD=tu_contraseña
HOST=tu_host
PORT=tu_puerto
DATABASE=tu_base_de_datos

# Conexión a PostgreSQL con SQLAlchemy y os
Para conectar a la base de datos PostgreSQL, se utilizan las librerías sqlalchemy y os. La conexión se define de la siguiente manera en el archivo main.py:

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('USER')
PWD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

connection_string = f'postgresql://{USER}:{PWD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(connection_string)

# Configuración de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='WebScraping_Esther/log/scraping.log',
                    filemode='a',
                    encoding='utf-8')


Resumen del Código de Web Scraping
El código realiza las siguientes acciones:

Conexión a la Base de Datos: Utiliza las credenciales almacenadas en el archivo .env para conectarse a PostgreSQL.
Extracción de Datos: Utiliza la librería requests para acceder a la web y BeautifulSoup para extraer y parsear las frases, autores, tags, y la información adicional de los autores.
Almacenamiento de Datos: Los datos extraídos se almacenan en un DataFrame de pandas y luego se envían a una tabla en la base de datos PostgreSQL utilizando SQLAlchemy.
Logging: Se utiliza la librería logging para registrar las actividades y errores durante la ejecución del script.











