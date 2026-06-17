from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.core.logging import LoggingMiddleware
from app.src import auth , groups


app = FastAPI(
    title="Split Smart⚡",
    lifespan=lifespan
)


# Adding Middleware
app.add_middleware(LoggingMiddleware)

# including the routers
app.include_router(auth.router)
app.include_router(groups.router)