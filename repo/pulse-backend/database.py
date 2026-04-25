import asyncio
from typing import Any, Dict, Optional

import logging
from redis.asyncio import Redis
from supabase import Client, create_client
import chromadb
from chromadb.config import Settings as ChromaSettings

from config import get_settings

logger = logging.getLogger("pulse.database")
settings = get_settings()

anon_client: Optional[Client] = None
service_client: Optional[Client] = None
redis_client: Optional[Redis] = None
chroma_client: Optional[chromadb.ClientAPI] = None


def get_anon_client() -> Client:
    global anon_client
    if anon_client is None:
        anon_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    return anon_client


def get_service_client() -> Client:
    global service_client
    if service_client is None:
        service_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return service_client


async def get_redis() -> Optional[Redis]:
    global redis_client
    if redis_client is None:
        if not settings.REDIS_URL:
            logger.warning("REDIS_URL is empty, running without Redis (features needing Redis will fail or fallback)")
            return None
        try:
            redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return None
    return redis_client

def get_chroma() -> chromadb.ClientAPI:
    global chroma_client
    if chroma_client is None:
        if settings.CHROMA_MODE == "memory":
            logger.info("Initializing ChromaDB in memory mode")
            chroma_client = chromadb.EphemeralClient()
        else:
            logger.info("Initializing ChromaDB in server mode")
            # Fallback to standard client if configured for server
            chroma_client = chromadb.HttpClient(host="localhost", port=8001)
    return chroma_client


async def run_supabase(method, *args, **kwargs) -> Dict[str, Any]:
    return await asyncio.to_thread(method, *args, **kwargs)
