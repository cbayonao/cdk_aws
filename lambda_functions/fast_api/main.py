#!/usr/bin/env python3
from fastapi import FastAPI
from mangum import Mangum


app = FastAPI(
    title="Un nombre al app",
    description="Descripción del app"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hola")
def read_root():
    return {"hola": "mundo"}


handler = Mangum(app, lifespan="off")