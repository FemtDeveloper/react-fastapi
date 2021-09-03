from fastapi import FastAPI
from database import Base, engine


app  = FastAPI()

Base.metadata.create_all(engine)


@app.post('/user')
def create_user():
    pass