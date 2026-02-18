from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import user, post  
from .routers import user, post, auth, vote

app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Welcome to my API"}