from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MenuFood API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReservationCreate(BaseModel):
    telegram_id: str
    restaurant_id: int
    party_size: int
    reservation_date: str
    reservation_time: str

@app.get("/api/restaurants")
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(models.Restaurant).filter(models.Restaurant.is_active == True).all()

@app.post("/api/reservations")
def create_reservation(data: ReservationCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.telegram_id == data.telegram_id).first()
    if not user:
        user = models.User(telegram_id=data.telegram_id, first_name="کاربر تلگرام")
        db.add(user)
        db.commit()
        db.refresh(user)

    new_reservation = models.TableReservation(
        user_id=user.id,
        restaurant_id=data.restaurant_id,
        party_size=data.party_size,
        reservation_date=data.reservation_date,
        reservation_time=data.reservation_time,
        status="pending"
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return {"status": "success", "message": "رزرو میز با موفقیت ثبت شد.", "reservation_id": new_reservation.id}