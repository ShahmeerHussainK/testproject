from fastapi import FastAPI
from app.database import database, engine, Base
from app.controllers import auth_controller, post_controller

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(auth_controller.router, prefix="/auth")
app.include_router(post_controller.router, prefix="/posts")
