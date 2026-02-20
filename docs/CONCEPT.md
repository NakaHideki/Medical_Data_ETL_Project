# 🏥 Medical Data ETL & API — プロジェクトコンセプト

## 1. プロジェクトの背景と動機

### 実務課題

医療現場では、**毎日100〜200件** の患者データが異なるテンプレート・フォーマット（CSV、PDF）で届き、スタッフが手動でSQL Serverに入力していた。

**発生していた具体的な問題：**

| 問題 | 影響 |
|------|------|
| 手動入力によるtypo（患者ID・金額のミス） | データ品質の低下 → 請求エラー |
| テンプレートごとにフォーマットが異なる | 入力者の判断負荷が高い |
| 一日の処理に数時間かかる | スタッフの時間コスト |
| 入力後のチェック体制がない | ミスが後工程まで伝搬 |

### このプロジェクトのアプローチ

**「手動入力をETLパイプラインで自動化し、クレンジング済みデータをAPIで提供する」** というアーキテクチャを設計・実装した。

```
Before:  CSV/PDF → 手動入力 → SQL Server（ミス混入リスク大）
After:   CSV → ETL自動処理 → PostgreSQL → REST API（バリデーション済み）
```

---

## 2. 設計思想

### 2.1 ETLパイプラインの設計

ETL（Extract-Transform-Load）パターンを採用した理由：

- **Extract**: データソースの形式に依存しない入口を作る
- **Transform**: データ品質を保証するバリデーション層を設ける
- **Load**: クリーンなデータのみをDBに投入する

```
                ┌──────────────────────────────────────────────┐
                │             Transform（5段階クレンジング）       │
  ┌──────────┐  │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │  ┌──────────┐
  │ Extract  │──▶│ │空白トリム│→│ID検証  │→│日付検証 │→│金額検証 │ │──▶│   Load   │
  │ CSV読込  │  │ └────────┘ └────────┘ └────────┘ └────────┘ │  │ DB投入   │
  └──────────┘  │                         ┌────────┐          │  └──────────┘
                │                         │重複排除 │          │
                │                         └────────┘          │
                └──────────────────────────────────────────────┘
```

**各クレンジングステップの理由：**

| ステップ | 実装 | 実務で発生していた問題 |
|---------|------|---------------------|
| 空白トリム | `str.strip()` | CSVエクスポート時に余分な空白が混入 |
| 患者ID検証 | `dropna(subset=["patient_id"])` | IDなしレコードは追跡不能 |
| 日付バリデーション | `pd.to_datetime(errors="coerce")` | 手入力で `invalid-date` 等が混入 |
| 金額バリデーション | `billed_amount > 0` | マイナス金額は請求エラー |
| 重複排除 | `drop_duplicates()` | 同一レコードの二重登録 |

### 2.2 REST API の設計

**リソース指向** でエンドポイントを設計し、HTTPメソッドで操作を表現：

```
GET    /                          → 患者データ一覧（サンプル）
GET    /patients/{patient_id}     → 特定患者をID指定で取得
GET    /patients?diagnosis=...    → 診断名・コストで患者を検索
POST   /patients                  → 新規患者データ登録
GET    /etl/run                   → ETLパイプライン実行
GET    /db/claims                 → DB格納済みの医療費レコード取得
POST   /db/load                   → クレンジング済みデータをDBに投入
```

**設計判断：**

- **パスパラメータ** (`/patients/P001`): 特定リソースの一意指定
- **クエリパラメータ** (`/patients?diagnosis=Diabetes&min_cost=10000`): フィルタ・検索条件
- **POST vs GET の使い分け**: データの作成・状態変更にはPOST、取得にはGET

### 2.3 データベース設計

SQLAlchemy ORMを採用し、Pythonクラスでテーブルを表現：

```python
class MedicalClaim(Base):
    __tablename__ = "medical_claims"
    
    id             = Column(Integer, primary_key=True)
    patient_id     = Column(String(10), nullable=False)   # 患者ID（必須）
    claim_date     = Column(Date, nullable=False)          # 請求日（必須）
    diagnosis_code = Column(String(20))                    # 診断コード（ICD-10）
    procedure_code = Column(Integer)                       # 処置コード（CPT）
    billed_amount  = Column(Numeric(10, 2))                # 請求金額
    provider_id    = Column(String(10))                    # 医療提供者ID
```

**ORM採用の理由：**

- SQLを直接書かずにPythonオブジェクトで操作 → 型安全性
- DB変更（PostgreSQL → MySQL 等）への対応がコード側の修正不要
- テーブル定義がコードに残り、スキーマのバージョン管理が可能

---

## 3. インフラ設計

### 3.1 Docker構成

**マルチステージビルド** でイメージサイズを最適化：

```dockerfile
# ステージ1: ビルド用（依存ライブラリのインストール）
FROM python:3.9-slim AS builder
# pip install で依存を /install にインストール

# ステージ2: 本番用（軽量）
FROM python:3.9-slim AS production
# builder からライブラリだけコピー（ビルドツールは含まない）
```

**メリット:**

- ビルドツール（gcc、pip等）を最終イメージに含めない → イメージサイズ削減
- セキュリティ面でも不要なツールがない方が攻撃対象が小さい

### 3.2 docker-compose によるオーケストレーション

```yaml
services:
  db:   PostgreSQL 15（ヘルスチェック付き）
  api:  FastAPIアプリ（db の起動完了を待って起動）
```

**ヘルスチェック + depends_on の理由：**

- DBが完全に起動する前にAPIが接続を試みると失敗する
- `pg_isready` でDBの起動完了を確認してからAPIを起動

### 3.3 CI/CD パイプライン

GitHub Actionsで自動テストを実現：

```
Push / PR to main
  → Checkout code
  → Setup Python 3.9
  → Install dependencies
  → Start PostgreSQL service container
  → Run pytest
```

**CI/CD導入の効果：**

- コードの変更ごとに自動テスト → リグレッション（退行バグ）防止
- PRレビュー時にテスト結果が表示される → レビュー効率向上
- 本番環境と同じDB（PostgreSQL）でテスト → 環境差異による問題を回避

---

## 4. 技術選定の理由

| 技術 | 選定理由 | 他の選択肢との比較 |
|------|---------|------------------|
| **FastAPI** | 自動ドキュメント生成、型ヒント統合、高パフォーマンス | Flask: 軽量だが型ヒント統合なし / Django: フルスタックで過剰 |
| **Pandas** | データ加工に特化、ETL処理に最適 | 純Python: 処理速度が遅い / PySpark: 小規模データには過剰 |
| **SQLAlchemy** | Python標準のORM、DB非依存 | 生SQL: 可読性低い / Django ORM: Django依存 |
| **PostgreSQL** | 型安全、JSON対応、業務用途に十分 | MySQL: 型が緩い / SQLite: 並行処理に弱い |
| **Docker** | 環境の再現性を保証 | venv: OS依存が残る / Vagrant: 重い |
| **GitHub Actions** | GitHubとの統合がスムーズ、無料枠あり | Jenkins: セルフホスト必要 / CircleCI: 設定が複雑 |
| **pytest** | Pythonテストのデファクトスタンダード | unittest: ボイラープレートが多い |

---

## 5. 学んだ技術概念

### バックエンド開発

- **REST API設計**: リソース指向URL、HTTPメソッドの使い分け、ステータスコード
- **依存性注入 (DI)**: FastAPIの`Depends()`によるDBセッション管理
- **ORMパターン**: Pythonクラスとデータベーステーブルのマッピング
- **データバリデーション**: Pandasを使った5段階のクレンジングパイプライン

### DevOps / インフラ

- **コンテナ化**: Dockerによる環境の再現性保証
- **マルチステージビルド**: イメージサイズの最適化
- **オーケストレーション**: docker-composeによる複数サービス管理
- **CI/CD**: GitHub Actionsによるテスト自動化
- **ヘルスチェック**: サービス間の起動順序制御

### テスト・品質

- **ユニットテスト**: ETL処理の各ステップを個別に検証
- **統合テスト**: FastAPIのTestClientでエンドポイントを検証
- **テスト自動化**: CI/CDでのpytest+PostgreSQL自動実行

---

## 6. 今後の拡張計画

| 優先度 | 機能 | 技術 |
|:---:|------|------|
| 🔴 高 | JWT認証によるAPI保護 | python-jose, OAuth2 |
| 🔴 高 | Redisキャッシュ | redis-py |
| 🟡 中 | 構造化ログ・監視 | Python logging, JSON formatter |
| 🟡 中 | 推論API（医療費異常検知） | scikit-learn, MLOps |
| 🟢 低 | Kubernetes デプロイ | GKE, K8s manifests |
| 🟢 低 | マイクロサービス分割 | gRPC, メッセージキュー |

---

## 7. 面談で話せるポイント

### Q: このプロジェクトで一番工夫した点は？

> **ETLパイプラインのクレンジング設計**です。実務で実際に発生していた問題（空白混入、マイナス金額、無効な日付、重複登録）をそれぞれバリデーションステップとして実装しました。各ステップは独立しているため、将来新しいバリデーションルールを追加する際も既存ロジックに影響しません。

### Q: なぜFastAPIを選びましたか？

> **型ヒントとの統合と自動ドキュメント生成**が理由です。Pydanticでリクエスト/レスポンスのスキーマを定義すると、バリデーションとSwagger UIでのドキュメントが自動で行われます。Flaskと比べて開発効率が高く、Django と比べてAPIに特化した軽量さがあります。

### Q: Docker / CI/CD の経験は？

> マルチステージビルドで本番用Dockerfileを書き、**ビルドステージと実行ステージを分離してイメージサイズを最適化**しました。docker-composeでAPI + PostgreSQLの複数サービスを管理し、**ヘルスチェックによる起動順序制御**も実装しています。CI/CDはGitHub Actionsで、push/PR時に**PostgreSQLサービスコンテナ付きの自動テスト**が実行されます。

### Q: テストはどう書いていますか？

> pytestで**ユニットテストと統合テスト**の両方を書いています。ETL処理は各クレンジングステップを個別にテスト（金額バリデーション、日付バリデーション、重複排除）、APIはFastAPIのTestClientを使ってエンドポイントの応答を検証しています。CIで毎回自動実行されるので、リグレッション防止にもなっています。
