from sqlalchemy.orm import Session
from models import Trade, TradeType
from schemas import TradeCreate
from datetime import date
from sqlalchemy import func

def create_trade(db: Session, trade: TradeCreate):
    # 입력 단위에 따라 실제 가격 계산
    real_price = trade.price * trade.price_unit
    fee_rate = trade.fee_rate if trade.type == "sell" else 0.0
    # 판매는 수수료 차감
    if trade.type == "sell":
        real_price = int(real_price * (1 - fee_rate / 100))
    db_trade = Trade(
        type=TradeType(trade.type),
        title=trade.title,
        quantity=trade.quantity,
        price=real_price,
        price_unit=trade.price_unit,
        date=trade.date,
        fee_rate=fee_rate
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_trades_by_date(db: Session, target_date: date):
    return db.query(Trade).filter(Trade.date == target_date).all()

def get_daily_summary(db: Session, target_date: date):
    # 판매, 구매 총합 계산
    total_sell = db.query(func.sum(Trade.price * Trade.quantity)).filter(Trade.type == TradeType.SELL, Trade.date == target_date).scalar() or 0
    total_buy = db.query(func.sum(Trade.price * Trade.quantity)).filter(Trade.type == TradeType.BUY, Trade.date == target_date).scalar() or 0
    profit = total_sell - total_buy
    profit_rate = (profit / total_buy * 100) if total_buy > 0 else None
    return {
        "total_sell": total_sell,
        "total_buy": total_buy,
        "profit": profit,
        "profit_rate": profit_rate
    } 