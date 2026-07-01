from fastapi import FastAPI
from app.routers import link_router
from app.core.handlers import setup_exception_handlers

app = FastAPI()
setup_exception_handlers(app)
app.include_router(link_router)


@app.get("/health")
def health():
    return {"status": "ok"}
