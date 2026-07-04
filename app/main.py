from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.core.logging import LoggingMiddleware
from app.src import auth, expenses , groups
from app.utils.exceptions.register import register_exception_handlers


app = FastAPI(
    title="Split Smart⚡",
    lifespan=lifespan
)


# Adding Middleware
app.add_middleware(LoggingMiddleware)

# including the routers
app.include_router(auth.router)
app.include_router(groups.router)
app.include_router(expenses.router)

# registering error handlers
register_exception_handlers(app)
