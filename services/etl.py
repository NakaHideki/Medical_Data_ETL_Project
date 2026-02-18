import pandas as pd

def load_csv(file_path: str):
    """CSVファイルを読み込み、Pandas DataFrameを返す"""
    df = pd.read_csv(file_path)
    return df

def clean_data(df):
    """データのクリーニング"""
    # 1. 空白をトリム
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    # 2. patient_idが空の行を除外
    df = df.dropna(subset=["patient_id"])
    # 3. 日付が不正な行を除外
    df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")
    df = df.dropna(subset=["claim_date"])
    # 4. 金額が0以下を除外
    df = df[df["billed_amount"] > 0]
    # 5. 完全な重複行を削除
    df = df.drop_duplicates()

    return df
