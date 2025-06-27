import sqlite3

db_path = "maple.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. fee_rate 컬럼이 없으면 추가
cur.execute("""
PRAGMA table_info(trades)
""")
columns = [row[1] for row in cur.fetchall()]
if "fee_rate" not in columns:
    cur.execute("ALTER TABLE trades ADD COLUMN fee_rate REAL DEFAULT 5.0")

# 2. 판매는 5%, 구매는 0%로 일괄 업데이트
cur.execute("UPDATE trades SET fee_rate = 5.0 WHERE type = 'sell'")
cur.execute("UPDATE trades SET fee_rate = 0.0 WHERE type = 'buy'")

conn.commit()
conn.close()

print("마이그레이션 완료: fee_rate 컬럼 추가 및 기존 데이터 업데이트")