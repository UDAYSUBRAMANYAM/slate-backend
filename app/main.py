from fastapi import FastAPI
from dotenv import load_dotenv

from app.db.base import Base
from app.db.session import engine
from app.routes import auth, knowledge, ai, public

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Slate  Second Brain")

app.include_router(auth.router)
app.include_router(knowledge.router)
app.include_router(ai.router)
app.include_router(public.router)
