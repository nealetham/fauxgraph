import os
from dotenv import load_dotenv
from app.api.v1 import node, edge

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=3600)
app.include_router(node.router)
app.include_router(edge.router)
