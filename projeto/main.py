from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI

from .routers import disciplinas, notas
from .database import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


app.include_router(disciplinas.router)
app.include_router(notas.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)