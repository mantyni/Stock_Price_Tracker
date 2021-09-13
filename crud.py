import models, schemas
from sqlalchemy.orm import Session


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def remove_user(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    db.delete(user)
    return db.commit()
    

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
