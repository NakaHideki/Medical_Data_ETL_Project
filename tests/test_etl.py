from services.etl import load_csv, clean_data

def test_load_csv():
    """CSVが正しく読み込めるか"""
    df = load_csv("data/sample_medical_data.csv")
    assert len(df) > 0

def test_clean_removes_negative_cost():
    """金額が0以下の行が削除されるか？"""
    df = load_csv("data/sample_medical_data.csv")
    df_clean = clean_data(df)
    assert (df_clean["billed_amount"] > 0).all()

def test_clean_removes_duplicates():
    """重複行が除去されるか？"""
    df = load_csv("data/sample_medical_data.csv")
    df_clean = clean_data(df)
    assert len(df_clean) < len(df)

def test_clean_removes_invalid_date():
    """不正な日付が削除されてるか？"""
    df = load_csv("data/sample_medical_data.csv")
    df_clean = clean_data(df)
    assert (df_clean["claim_date"].notna()).all()
