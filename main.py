from fastapi import FastAPI
from fastapi import Depends
from services.database import init_db, get_db, MedicalClaim
from sqlalchemy.orm import Session
from services.etl import load_csv, clean_data  

app = FastAPI()  # APIアプリを作る
init_db()  # 起動時にテーブルを自動作成


@app.get("/")  # GETリクエストが / に来たら
def hello():
    return [
        {"patient_id": "P001", "name": "Taro Yamada", "age": 45, "gender": "Male", "diagnosis": "Common Cold", "treatment": "Rest and fluids", "cost": 5000},
        {"patient_id": "P002", "name": "Hanako Sato", "age": 32, "gender": "Female", "diagnosis": "Hypertension", "treatment": "Medication and lifestyle changes", "cost": 12000},
        {"patient_id": "P003", "name": "Kenji Tanaka", "age": 67, "gender": "Male", "diagnosis": "Diabetes", "treatment": "Medication and diet management", "cost": 15000},
        {"patient_id": "P004", "name": "Yuki Suzuki", "age": 28, "gender": "Female", "diagnosis": "Asthma", "treatment": "Inhaler and regular check-ups", "cost": 8000},
        {"patient_id": "P005", "name": "Hiroshi Ito", "age": 55, "gender": "Male", "diagnosis": "Arthritis", "treatment": "Physical therapy and medication", "cost": 10000} 
    ]

@app.get("/patients/{patient_id}") # URLの{patient_id}が
def get_patient(patient_id:str):   # ↑ ここに自動で入る
    # 全患者データから一致するIDを探す
    # patient_id = "P001" として使える
    patients = [
        {"patient_id": "P001", "name": "Taro Yamada", "age": 45, "gender": "Male", "diagnosis": "Common Cold", "treatment": "Rest and fluids", "cost": 5000},
        {"patient_id": "P002", "name": "Hanako Sato", "age": 32, "gender": "Female", "diagnosis": "Hypertension", "treatment": "Medication and lifestyle changes", "cost": 12000},
        {"patient_id": "P003", "name": "Kenji Tanaka", "age": 67, "gender": "Male", "diagnosis": "Diabetes", "treatment": "Medication and diet management", "cost": 15000},
        {"patient_id": "P004", "name": "Yuki Suzuki", "age": 28, "gender": "Female", "diagnosis": "Asthma", "treatment": "Inhaler and regular check-ups", "cost": 8000},
        {"patient_id": "P005", "name": "Hiroshi Ito", "age": 55, "gender": "Male", "diagnosis": "Arthritis", "treatment": "Physical therapy and medication", "cost": 10000} 
    ]
    
    for patient in patients:
        if patient["patient_id"] == patient_id:
            return patient
    
    # 見つからなかった場合
    return {"error": "Patient not found"}, 404

@app.get("/patients") #GET /patients というURLを登録するデコレータ  
def search_patients(diagnosis: str = None, min_cost: int = 0):#関数の引数 = クエリパラメータになる 
    patients = [
        {"patient_id": "P001", "name": "Taro Yamada", "age": 45, "gender": "Male", "diagnosis": "Common Cold", "treatment": "Rest and fluids", "cost": 5000},
        {"patient_id": "P002", "name": "Hanako Sato", "age": 32, "gender": "Female", "diagnosis": "Hypertension", "treatment": "Medication and lifestyle changes", "cost": 12000},
        {"patient_id": "P003", "name": "Kenji Tanaka", "age": 67, "gender": "Male", "diagnosis": "Diabetes", "treatment": "Medication and diet management", "cost": 15000},
        {"patient_id": "P004", "name": "Yuki Suzuki", "age": 28, "gender": "Female", "diagnosis": "Asthma", "treatment": "Inhaler and regular check-ups", "cost": 8000},
        {"patient_id": "P005", "name": "Hiroshi Ito", "age": 55, "gender": "Male", "diagnosis": "Arthritis", "treatment": "Physical therapy and medication", "cost": 10000} 
    ]

    results = [] #空のリストを用意。条件に合う患者をここに追加していく

    for p in patients:
        if min_cost > 0 and p["cost"] < min_cost:
            # 2つの条件を両方チェック（and）
            #ユーザーが最低金額を指定した？
            #この患者のコストが基準より低い？
            continue
        if diagnosis and p["diagnosis"] != diagnosis:
            #ユーザーが診断名を指定した？
            #この患者の診断名が一致しない？
            continue
        results.append(p)
    return results

@app.post("/patients") #POSTリクエスト = データを新規作成
def add_patient(patient: dict):
    #受け取ったデータをそのまま返す(本来はDBに保存する)
    return {"message": "患者データを登録しました", "data": patient}

@app.get("/etl/run")
def run_etl():
    """ETLプロセスを実行するエンドポイント"""
    df = load_csv("data/sample_medical_data.csv")
    raw_count = len(df)

    df_clean = clean_data(df)
    clean_count = len(df_clean)

    return{
        "raw_count": raw_count,
        "clean_count": clean_count,
        "removed": raw_count - clean_count,
        "data": df_clean.to_dict(orient="records")
    }

@app.get("/db/claims")
def get_claims_from_db(db: Session = Depends(get_db)):
    """DBから全レコードを取得"""
    claims = db.query(MedicalClaim).all()
    return [
        {
            "patient_id": c.patient_id,
            "claim_date": str(c.claim_date),
            "diagnosis_code": c.diagnosis_code,
            "billed_amount": float(c.billed_amount) if c.billed_amount else 0,
        }
        for c in claims
    ]

@app.post("/db/load")
def load_to_db(db: Session = Depends(get_db)):
    """ETLでクリーンしたデータをDBに投入"""
    from services.etl import load_csv, clean_data
    df = load_csv("data/sample_medical_data.csv")
    df_clean = clean_data(df)
    
    for _, row in df_clean.iterrows():
        claim = MedicalClaim(
            patient_id=row["patient_id"],
            claim_date=row["claim_date"],
            diagnosis_code=row["diagnosis_code"],
            procedure_code=int(row["procedure_code"]),
            billed_amount=float(row["billed_amount"]),
            provider_id=row["provider_id"],
        )
        db.add(claim)
    db.commit()
    return {"message": f"{len(df_clean)}件をDBに登録しました"}



"""
エンドポイントとは？ = 「APIの入口のURL」
レストラン（= API）
├── 正面入口（/）           → メニュー一覧を見る
├── 個室入口（/patients/P001）→ 特定の患者を見る
├── 検索窓口（/patients?...） → 条件で探す
└── 受付窓口（POST /patients）→ 新しいデータを登録
"""