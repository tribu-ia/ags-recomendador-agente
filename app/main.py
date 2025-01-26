import logging
import os
from typing import Optional, Dict

from dotenv import load_dotenv
from fastapi import Request, FastAPI, HTTPException, Query, Body
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.db_manager.elasticsearch_store import MyElasticsearchVectorStore
from app.models.investigador import JsonDataPayload, ElasticsearchQueryPayload, PaginatedResponse, InvestigadorPayload

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="Bella Bot Assistant",
    description="API for Bella Bot Assistant",
    version="1.0.0",
    # Aquí defines el prefijo base para todas las rutas
    root_path="/api/agents-recommendations"
)

db_config = {
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Instancias globales
es_store = MyElasticsearchVectorStore()


@app.post("/upload-json/elasticsearch")
async def upload_json_elasticsearch(payload: JsonDataPayload):
    try:
        json_items = payload.data[0]['json']['data']

        if not json_items:
            raise HTTPException(
                status_code=400,
                detail="No se encontraron datos válidos en el JSON"
            )

        # Procesar el JSON con Elasticsearch
        es_documents = es_store.process_json_data(json_items)

        return {
            "status": "success",
            "message": "JSON procesado correctamente",
            "elasticsearch_items": len(es_documents),
            "total_items_received": len(json_items)
        }
    except Exception as e:
        logger.error(f"Error al procesar el JSON: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el JSON: {str(e)}")


@app.post("/query/hybrid-search")
async def process_hybrid_search(payload: ElasticsearchQueryPayload):
    try:
        if not payload.query.strip():
            raise HTTPException(status_code=400, detail="La consulta no puede estar vacía")

        results = es_store.search(
            query=payload.query,
            k=payload.k
        )

        if not results:
            return {
                "query": payload.query,
                "results": [],
                "message": "No se encontraron resultados para la consulta"
            }

        return {
            "query": payload.query,
            "results": results,
            "message": "Búsqueda híbrida exitosa"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {str(e)}")


@app.post("/send/elasticsearch")
async def upload_json_elasticsearch(payload: JsonDataPayload):
    try:
        # Extraer directamente el array de datos del primer elemento
        json_items = payload.data[0]['json']['data']

        if not json_items:
            raise HTTPException(
                status_code=400,
                detail="No se encontraron datos válidos en el JSON"
            )

        # Procesar el JSON con Elasticsearch
        es_documents = es_store.process_json_data(json_items)

        return {
            "status": "success",
            "message": "JSON procesado correctamente",
            "elasticsearch_items": len(es_documents),
            "total_items_processed": len(json_items)
        }
    except Exception as e:
        logger.error(f"Error al procesar el JSON: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el JSON: {str(e)}")


@app.post("/investigadores")
async def create_investigador(payload: InvestigadorPayload):
    try:
        investigador_data = {
            "name": payload.name,
            "email": payload.email,
            "phone": payload.phone,
            "agent_id": payload.agent,
            "github_username": payload.github_username,
            "linkedin_profile": payload.linkedin_profile
        }

        result = await db_manager.create_investigador(investigador_data)

        return {
            "status": "success",
            "message": "Investigador registrado correctamente",
            "data": result
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error al crear investigador: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear investigador: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled exception: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"}
        )

@app.get("/stats")
async def get_stats():
    """Obtiene estadísticas de agentes e investigadores"""
    try:
        stats = await db_manager.get_stats()
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al obtener estadísticas"
        )
