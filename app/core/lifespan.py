from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import configs, database , redis
# Explicit model registration
from app.src.auth import models as auth_models
from app.src.groups import models as groups_models
from app.src.expenses import models as expenses_models
from app.src.payments import models as payments_models

@asynccontextmanager
async def lifespan(app : FastAPI):
    # Startup
    database.create_tables_and_db()
    app.state.redis = await redis.get_redis(host=configs.settings.redis_host , max_connections= configs.settings.redis_max_connections, port=configs.settings.redis_port)
    print("Redis Connected Successfully")
    print("DB and tables created successfully")
    yield
    # Shutdown
    if hasattr(app.state, 'redis'):
        await app.state.redis.aclose()