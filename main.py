from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from schemas import TradeCreate, TradeRead
from crud import create_trade, get_trades_by_date, get_daily_summary
from typing import List
from datetime import date
from models import Trade

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Maple Story 거래 API"}

@app.on_event("startup")
def on_startup():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/trades/", response_model=TradeRead)
def add_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    return create_trade(db, trade)

@app.get("/trades/{target_date}", response_model=List[TradeRead])
def read_trades(target_date: date, db: Session = Depends(get_db)):
    return get_trades_by_date(db, target_date)

@app.get("/summary/{target_date}")
def read_summary(target_date: date, db: Session = Depends(get_db)):
    return get_daily_summary(db, target_date)

@app.delete("/trades/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="거래 내역을 찾을 수 없습니다.")
    db.delete(trade)
    db.commit()
    return {"ok": True} 