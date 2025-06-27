from sqlalchemy import Column, Integer, String, Date, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import date

Base = declarative_base()

class TradeType(enum.Enum):
    SELL = "sell"
    BUY = "buy"

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(TradeType), nullable=False)  # 판매/구매
    title = Column(String, nullable=False)          # 물품 제목
    quantity = Column(Integer, nullable=False)      # 수량
    price = Column(Integer, nullable=False)         # 가격(실제 메소 단위)
    price_unit = Column(Integer, nullable=False)    # 입력 단위(1 또는 10000)
    date = Column(Date, default=date.today, nullable=False)  # 거래 날짜
    fee_rate = Column(Float, default=5.0, nullable=False)    # 거래 수수료율(%) 