from sqlalchemy.sql.type_api import INDEXABLE
import services, schemas
from struct import pack
from typing import List
from fastapi import FastAPI, HTTPException
from starlette import status
from database import get_db, Base, engine
from services import get_user_by_email, new_user, authenticate_user,create_token, get_current_user,lead_create, lead_delete, lead_update
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from schemas import UserCreate
from fastapi.security import OAuth2PasswordRequestForm


app  = FastAPI()

Base.metadata.create_all(engine)


@app.post('/api/user')
async def create_user(user: UserCreate, db: Session=Depends(get_db)):
    db_user = await get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    await new_user(user, db)
    return await create_token(user)

@app.post('/api/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Inavalid Credentials')
    return await create_token(user)

@app.get('/api/users/{id}', response_model= schemas.User)
async def get_user(id: int, user: schemas.User =  Depends(get_current_user), db: Session= Depends(get_db)):
    return user

@app.post('/api/leads', response_model=schemas.Lead)
async def create_lead(lead: schemas.LeadCreate, 
                    user: schemas.User=Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    return await lead_create(user=user, db=db, lead=lead)    

@app.get('/api/leads', response_model=List[schemas.Lead])
async def get_leads( user: schemas.User=Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    return await services.get_leads(user=user, db=db)

@app.get('/api/leads/{lead_id}')
async def get_lead(lead_id: int, user: schemas.User=Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    return await services.get_lead_by_id(lead_id, user, db)

@app.delete('/api/{lead_id}', status_code= 204)
async def delete_lead(lead_id: int, user: schemas.User=Depends(get_current_user), 
                    db: Session = Depends(get_db)):    
    await lead_delete(lead_id, user, db)
    return 'Lead sucessfully deleted'

@app.put('/api/{lead_id}', status_code= 200)
async def update_lead(lead_id: int, lead: schemas.LeadCreate, user: schemas.User=Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    await lead_update(lead_id, lead, user, db)
    return 'Lead sucessfully Updated'

@app.get('/api')
async def root():
    return {"message": "This is my response"}