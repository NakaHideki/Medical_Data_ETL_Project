# 🏥 Medical Data ETL & API Service

> **医療費データの自動ETLパイプラインとREST API**
> 医療現場で発生する患者データ・医療費データを自動で抽出・加工・格納し、APIとして提供するサービス

[![CI Pipeline](https://github.com/NakaHideki/Medical_Data_ETL_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/NakaHideki/Medical_Data_ETL_Project/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)

---

## 📋 概要

医療現場では、毎日100〜200件の患者データがCSVやPDFなど統一されていないフォーマットで届き、手動でデータベースに入力していました。このプロジェクトは、その手動作業を **ETLパイプライン** で自動化し、クレンジング済みデータをREST APIで提供するシステムです。

### 解決した課題

| Before（従来） | After（このプロジェクト） |
|:---:|:---:|
| 手動でCSV/PDFからDB入力 | ETLパイプラインで自動処理 |
| 入力ミス（typo・金額ミス）が頻発 | バリデーション＋自動クレンジング |
| 処理遅延（100-200件/日を手作業） | API経由で即時処理 |
| テストなし | pytest による自動テスト |
| ローカル環境依存 | Docker + CI/CD で再現可能 |

---

## 🏗️ アーキテクチャ

```
┌──────────────┐     ┌──────────────────────────────────────────┐
│   CSV Data   │────▶│          FastAPI Application              │
│  (医療費データ) │     │  ┌────────┐  ┌───────────┐  ┌────────┐ │
└──────────────┘     │  │Extract │─▶│Transform  │─▶│  Load  │ │
                     │  │CSV読込  │  │クレンジング │  │DB投入   │ │
                     │  └────────┘  └───────────┘  └────┬───┘ │
                     │                                   │     │
                     │  ┌──────────────────────────────┐ │     │
                     │  │     REST API Endpoints       │ │     │
                     │  │  GET /  POST /patients  ...  │ │     │
                     │  └──────────────────────────────┘ │     │
                     └───────────────────────────────┬───┘     │
                                                     │         │
                                                     ▼         │
                                              ┌──────────────┐ │
                                              │  PostgreSQL  │◀┘
                                              │   Database   │
                                              └──────────────┘
```

---

## 🚀 技術スタック

| カテゴリ | 技術 | 用途 |
|---------|------|------|
| **Backend** | FastAPI (Python) | REST API フレームワーク |
| **ETL** | Pandas | データ抽出・加工・クレンジング |
| **ORM** | SQLAlchemy | データベース操作 |
| **Database** | PostgreSQL 15 | データ永続化 |
| **Container** | Docker + docker-compose | 環境構築・オーケストレーション |
| **CI/CD** | GitHub Actions | 自動テスト |
| **Test** | pytest | ユニットテスト・統合テスト |

---

## 📡 API エンドポイント

| Method | Path | 説明 |
|--------|------|------|
| `GET` | `/` | サンプル患者データ一覧を取得 |
| `GET` | `/patients/{patient_id}` | 特定の患者データをIDで取得 |
| `GET` | `/patients?diagnosis=...&min_cost=...` | 診断名・コストで患者を検索 |
| `POST` | `/patients` | 新規患者データを登録 |
| `GET` | `/etl/run` | ETLパイプラインを実行（CSV → クレンジング） |
| `GET` | `/db/claims` | DBから全医療費レコードを取得 |
| `POST` | `/db/load` | クレンジング済みデータをDBに投入 |

### Swagger UI

起動後、`http://localhost:8000/docs` でインタラクティブなAPI文書が自動生成されます。

---

## 🔧 ETL パイプライン

CSVデータに対して5段階のクレンジングを実施：

1. **空白トリム** — 文字列フィールドの前後空白を除去
2. **患者ID検証** — `patient_id` が空の行を除外
3. **日付バリデーション** — 無効な日付（`invalid-date` 等）を除外
4. **金額バリデーション** — `billed_amount` が0以下の行を除外
5. **重複排除** — 完全に一致する重複行を削除

### 入力データ例 → クレンジング結果

```
入力: 15件（不正データ含む）
  ├── 金額がマイナス (P005: -50.00) → 除外
  ├── patient_id が空 → 除外  
  ├── 日付が "invalid-date" (P008) → 除外
  ├── 完全重複行 (P003) → 除外
  └── 空白を含むデータ → トリム
出力: 10件（クリーンデータ）
```

---

## 🐳 セットアップ & 実行

### Docker Compose（推奨）

```bash
# クローン
git clone git@github.com:NakaHideki/Medical_Data_ETL_Project.git
cd medical-data-api

# 起動（API + PostgreSQL）
docker compose up --build

# 動作確認
curl http://localhost:8000/
curl http://localhost:8000/etl/run
curl -X POST http://localhost:8000/db/load
curl http://localhost:8000/db/claims
```

### ローカル開発

```bash
# 依存インストール
pip install -r requirements.txt

# PostgreSQL を別途起動しておく（またはdocker compose up db のみ）
docker compose up db -d

# API起動
uvicorn main:app --reload

# テスト実行
python -m pytest tests/ -v
```

---

## 🧪 テスト

```bash
# 全テスト実行
python -m pytest tests/ -v

# テスト内容
# test_api.py   — APIエンドポイントの統合テスト（GET /, GET /patients/P001, GET /etl/run）
# test_etl.py   — ETLパイプラインのユニットテスト（CSV読込、金額/日付/重複のクレンジング）
```

---

## 🐳 Docker 構成

### マルチステージビルド (`Dockerfile`)

```
ステージ1: builder     → 依存ライブラリのインストール
ステージ2: production  → 軽量な本番イメージ（ビルドツール不含）
```

### docker-compose (`compose.yml`)

```
services:
  db   → PostgreSQL 15（ヘルスチェック付き）
  api  → FastAPI アプリ（db の起動完了を待って起動）
```

---

## ⚙️ CI/CD

GitHub Actions でmainブランチへのpush/PR時に自動実行：

1. **Checkout** — コード取得
2. **Python Setup** — Python 3.9 環境セットアップ
3. **Install** — 依存ライブラリインストール
4. **Test** — PostgreSQLサービスコンテナ起動 + pytest 実行

---

## 📁 プロジェクト構成

```
medical-data-api/
├── main.py                 # FastAPI アプリケーション（エンドポイント定義）
├── services/
│   ├── etl.py              # ETLパイプライン（CSV読込 + 5段階クレンジング）
│   └── database.py         # SQLAlchemy ORM（PostgreSQL接続 + テーブル定義）
├── tests/
│   ├── test_api.py         # APIエンドポイントの統合テスト
│   └── test_etl.py         # ETL処理のユニットテスト
├── data/
│   └── sample_medical_data.csv  # サンプル医療費データ（15件）
├── docs/
│   ├── CONCEPT.md          # プロジェクトのコンセプトと設計思想
│   ├── PROJECT_BACKGROUND.md   # プロジェクト背景（実務との対応）
│   ├── LEARNING_LOG.md     # 学習記録
│   ├── LESSON_PLAN.md      # 学習プラン
│   └── CLAUDE_CODE_PROMPTS.md  # 開発プロンプト集
├── Dockerfile              # 本番用マルチステージビルド
├── Dockerfile.simple       # 開発用シンプルビルド
├── compose.yml             # Docker Compose（API + PostgreSQL）
├── .github/workflows/
│   └── ci.yml              # GitHub Actions CI/CDパイプライン
├── pyproject.toml          # プロジェクト設定・依存管理
├── requirements.txt        # pip依存パッケージ
└── .gitignore
```

---

## 👤 Author

**Hideki Nakazawa**

- GitHub: [@NakaHideki](https://github.com/NakaHideki)
