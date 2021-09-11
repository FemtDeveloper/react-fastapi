from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from starlette import status
import models, schemas
from sqlalchemy.orm.session import Session
from database import Base, engine, get_db
from passlib import hash
from jose import jwt, JWTError


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
oauth2schema = OAuth2PasswordBearer(tokenUrl='/api/token')


def create_database():
    return Base.metadata.create_all(bind= engine)


async def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def new_user(user: schemas.UserCreate, db: Session):
    user_obj = models.User(email = user.email, hashed_password = hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def authenticate_user(email: str, password: str, db: Session):
    user = await get_user_by_email(db=db, email=email)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), SECRET_KEY)
    return dict(access_token= token, token_type = 'bearer')


async def get_current_user(db: Session= Depends(get_db), token: str = Depends(oauth2schema)):
    try:
        payload =  jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user =  db.query(models.User).get(payload['id'])
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Username or Password')
    return schemas.User.from_orm(user)

async def get_user_by_id(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()

async def lead_create(user: schemas.User, db: Session, lead: schemas.LeadCreate):
    lead= models.Lead(**lead.dict(), owner_id= user.id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return schemas.Lead.from_orm(lead)

async def get_leads(user: schemas.User, db: Session):
    leads =  db.query(models.Lead).filter_by(owner_id=user.id)
    return list(map(schemas.Lead.from_orm, leads))

async def _lead_selector(lead_id: int, user: schemas.User, db: Session):
    lead = db.query(models.Lead).filter_by(owner_id= user.id).filter(models.Lead.id== lead_id).first()
    if lead is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Lead doesn´t exists')
    return lead

async def get_lead_by_id(lead_id: int, user: schemas.User, db: Session):
    lead = await _lead_selector(lead_id=lead_id, user=user, db=db)
    return schemas.Lead.from_orm(lead)


async def lead_delete(lead_id: int, user: schemas.User, db: Session):
    lead = await _lead_selector(lead_id, user, db)
    db.delete(lead)
    db.commit()
    

async def lead_update(lead_id: int, lead: schemas.LeadCreate, user: schemas.User, db: Session):
    lead_db =  await _lead_selector(lead_id, user, db)
    lead_db.first_name =  lead.first_name
    lead_db.last_name =  lead.last_name
    lead_db.company =  lead.company
    lead_db.note = lead.note
    lead_db.email =  lead.email
    lead_db.date_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(lead_db)
    return schemas.Lead.from_orm(lead_db)

