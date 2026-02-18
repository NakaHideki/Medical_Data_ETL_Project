import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base

# 環境変数からDB接続URL取得（compose.ymlで設定したもの）
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://medical_user:medical_pass@localhost:5432/medical_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# テーブル定義（ORM = Pythonクラスでテーブルを表現）
class MedicalClaim(Base):
    __tablename__ = "medical_claims"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(10), nullable=False)
    claim_date = Column(Date, nullable=False)
    diagnosis_code = Column(String(20))
    procedure_code = Column(Integer)
    billed_amount = Column(Numeric(10, 2))
    provider_id = Column(String(10))

def init_db():
    """テーブルを作成する"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """DBセッションを取得する（リクエストごとに使い回す）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()