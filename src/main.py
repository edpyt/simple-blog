from fastapi import FastAPI

from src.api.routes import blog

app = FastAPI()

app.include_router(blog.router)
