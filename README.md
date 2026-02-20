# Medical Data ETL & API

医療費データのETL処理とAPI提供を行うプロジェクト。

前職で毎日100〜200件の患者データを手動でDBに入力していた経験をもとに、その作業を自動化するETLパイプラインをPythonで構築しました。

[![CI Pipeline](https://github.com/NakaHideki/Medical_Data_ETL_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/NakaHideki/Medical_Data_ETL_Project/actions/workflows/ci.yml)

## やっていること

1. CSVから医療費データを読み込む（Extract）
2. 不正データをクレンジングする（Transform）
3. PostgreSQLに投入する（Load）
4. 格納したデータをREST APIで提供する

## 使った技術

- **Python / FastAPI** — API
- **Pandas** — ETL処理
- **SQLAlchemy** — ORM（PostgreSQL）
- **Docker / docker-compose** — 環境構築
- **GitHub Actions** — CI（自動テスト）
- **pytest** — テスト

## APIエンドポイント

```
GET  /                       患者データ一覧
GET  /patients/{patient_id}  特定の患者を取得
GET  /patients?diagnosis=... 診断名・コストで検索
POST /patients               新規患者登録
GET  /etl/run                ETL実行（CSV → クレンジング）
POST /db/load                クレンジング済みデータをDBに投入
GET  /db/claims              DBから全レコード取得
```

起動後 `http://localhost:8000/docs` でSwagger UIが使えます。

## ETLのクレンジング内容

CSVデータに対して以下を処理しています：

- 文字列の前後の空白を除去
- patient_idが空の行を除外
- 日付が不正な行を除外（`invalid-date` など）
- 金額が0以下の行を除外
- 完全な重複行を削除

## セットアップ

### Docker Compose（推奨）

```bash
git clone git@github.com:NakaHideki/Medical_Data_ETL_Project.git
cd medical-data-api

docker compose up --build
```

### ローカル

```bash
pip install -r requirements.txt

# PostgreSQLだけ先に起動
docker compose up db -d

uvicorn main:app --reload
```

## テスト

```bash
python -m pytest tests/ -v
```

- `test_api.py` — エンドポイントの動作確認
- `test_etl.py` — クレンジング処理の検証

## Docker構成

- `Dockerfile` — マルチステージビルド（本番用）
- `compose.yml` — API + PostgreSQL（ヘルスチェック付き）

## ディレクトリ構成

```
medical-data-api/
├── main.py              # FastAPIアプリ
├── services/
│   ├── etl.py           # ETL処理
│   └── database.py      # DB接続・テーブル定義
├── tests/
│   ├── test_api.py
│   └── test_etl.py
├── data/
│   └── sample_medical_data.csv
├── docs/                # ドキュメント
├── Dockerfile
├── compose.yml
├── .github/workflows/
│   └── ci.yml
├── pyproject.toml
└── requirements.txt
```

## 詳細

プロジェクトの背景や設計の考え方については [docs/CONCEPT.md](docs/CONCEPT.md) を参照してください。
