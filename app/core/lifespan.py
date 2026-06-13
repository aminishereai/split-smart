from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import configs, database , redis

@asynccontextmanager
async def lifespan(app : FastAPI):
    try:
        database.create_tables_and_db()
        app.state.redis = redis.get_redis(host=configs.settings.redis_host , max_connections= configs.settings.redis_max_connections, port=configs.settings.redis_port)
        yield
        print("Redis Connected Successfyully")
        print("Db and tables created successfully")
    finally :
        app.state.redis.aclose()