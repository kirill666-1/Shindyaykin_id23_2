from fastapi import FastAPI
from app.api import auth, tsp
from app.db.base import Base
from app.db.session import engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tsp.router, prefix="/tsp", tags=["tsp"])