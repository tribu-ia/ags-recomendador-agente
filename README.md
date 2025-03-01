# Backend de Investigación AGS

Una aplicación backend desarrollada con FastAPI que proporciona servicios de recomendación para agentes de IA utilizando Elasticsearch para búsqueda vectorial y procesamiento semántico.

## Características

- Almacenamiento y recuperación de datos de agentes de IA con capacidades de búsqueda vectorial
- Búsqueda híbrida con puntuación de similitud
- Procesamiento de datos JSON e integración con Elasticsearch
- Preprocesamiento de texto y segmentación semántica
- Sistema de registro de Investigadores
- Dockerizado para facilitar el despliegue

## Stack Tecnológico

- **Python 3.12**
- **FastAPI** - Framework web moderno y rápido
- **Elasticsearch** - Almacén vectorial y motor de búsqueda
- **OpenAI Embeddings** - Para generación de embeddings de texto
- **NLTK** - Herramientas de procesamiento de lenguaje natural
- **SQLAlchemy** - ORM para operaciones de base de datos
- **Docker** - Contenedorización

## Comenzando

### Requisitos previos

- Python 3.12+
- Docker y Docker Compose (opcional)
- Instancia de Elasticsearch
- Clave API de OpenAI

### Configuración del entorno

Crea un archivo `.env` en el directorio raíz con las siguientes variables:

```
# Configuración de la base de datos
DB_NAME=nombre_de_tu_bd
DB_USER=usuario_de_tu_bd
DB_PASSWORD=contraseña_de_tu_bd
DB_HOST=host_de_tu_bd
DB_PORT=5432

# Configuración de Elasticsearch
ES_URL=http://tu_host_elasticsearch:9200

# API de OpenAI
OPENAI_API_KEY=tu_clave_api_openai
```

### Instalación

#### Usando Docker

La forma más sencilla de ejecutar la aplicación es usando Docker:

```bash
# Construir la imagen Docker
docker build -t ags-investigacion-back .

# Ejecutar el contenedor
docker run -p 8000:8000 --env-file .env ags-investigacion-back
```

#### Instalación manual

1. Clona este repositorio:
```bash
git clone https://github.com/tu-repo/ags-investigacion-back.git
cd ags-investigacion-back
```

2. Crea un entorno virtual y actívalo:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints de la API

La API es accesible en la ruta base `/api/agents-recommendations`.

### Gestión de datos

- `POST /upload-json/elasticsearch` - Subir y procesar datos JSON en Elasticsearch
- `POST /send/elasticsearch` - Endpoint alternativo para procesamiento de datos JSON

### Búsqueda

- `POST /query/hybrid-search` - Realizar búsqueda híbrida en datos de agentes

### Gestión de usuarios

- `POST /investigadores` - Registrar un nuevo investigador

### Sistema

- `GET /health` - Endpoint de comprobación de salud
- `GET /stats` - Estadísticas del sistema

## Modelos de datos

### Agente de IA

El sistema trabaja con datos de agentes de IA que incluyen:
- Información básica (nombre, categoría, etc.)
- Descripciones (corta y larga)
- Características y casos de uso
- Enlaces a medios (logo, imagen, video)
- Metadatos (votos positivos, estado destacado)

### Investigador

Los usuarios que investigan agentes de IA pueden registrarse con:
- Información personal (nombre, email, teléfono)
- Perfiles profesionales (GitHub, LinkedIn)
- ID del agente seleccionado

## Implementación de búsqueda vectorial

La aplicación utiliza embeddings de OpenAI para crear representaciones vectoriales de datos de agentes, permitiendo capacidades de búsqueda semántica a través de Elasticsearch.

El preprocesamiento de texto incluye:
- Normalización y eliminación de caracteres especiales
- Tokenización
- Eliminación de palabras vacías (stopwords)
- Stemming
- Segmentación semántica

## Desarrollo

### Estructura del proyecto

```
ags-investigacion-back/
├── app/
│   ├── db_manager/
│   │   ├── elasticsearch_store.py
│   │   └── text_processor.py
│   ├── models/
│   │   └── investigador.py
│   ├── __init__.py
│   └── main.py
├── .env
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

### Añadir nuevas características

- Añade nuevos endpoints en `app/main.py`
- Crea nuevos modelos en el directorio `app/models/`
- Extiende los gestores de base de datos en `app/db_manager/`

## Licencia

[Incluye tu información de licencia aquí]

## Contacto

[Tu información de contacto]