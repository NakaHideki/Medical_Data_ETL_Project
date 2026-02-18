# 🏥 医療費データAPIプロジェクト - 面談対策レッスンプラン

## 🎯 ゴール
SES面談で「概念は理解しています。直近のミニプロジェクトでも触りました」と答えられるレベルになる。

---

## 🛠 環境構成

| ツール | 役割 |
|--------|------|
| **Antigravity (このチャット)** | 概念説明、骨組み提示、コードレビュー、面談練習 |
| **Claude Code (ターミナル)** | 実際のコーディング、テスト実行、デバッグ |

---

## 🧑‍💻 チーム設定（現場シミュレーション）

あなたは **新メンバーとしてチームにジョイン** した設定です。

| メンバー | 役割 | 担当 |
|---------|------|------|
| **あなた** | Junior Backend Engineer | API開発、テスト、認証、CI/CD |
| **Tanaka さん (AI同僚)** | Senior Engineer | ETLコア処理、DBモデル（先にコード書き済み） |
| **Suzuki さん (AI同僚)** | DevOps Engineer | Dockerfile、監視設定（先にコード書き済み） |

> Tanakaさん・Suzukiさんのコードは各Stepで提供されます。
> あなたはそのコードを**読み解き、自分のコードと統合する**必要があります。

---

## 📋 学習フロー（各Step共通）

```
1. 概念説明     → Antigravityで説明を受ける
2. 骨組み提示   → ファイル構成とスケルトン（中身は空）を受け取る
3. 自力実装     → Claude Codeで自分でコードを書く
4. コードレビュー → Antigravityに貼ってレビューを受ける
5. 同僚統合     → 同僚のコードとマージ・統合する
6. 面談回答練習  → この技術について聞かれた時の答え方を確認
```

---

## 📅 Day 1（今日）

### Step 1: FastAPIでREST API設計 (1.5時間)
**学べること:** REST API設計、エンドポイント設計、リクエスト/レスポンス設計

**概念キーワード:**
- REST (Representational State Transfer)
- HTTPメソッド (GET, POST, PUT, DELETE)
- ステータスコード (200, 201, 400, 404, 500)
- パスパラメータ vs クエリパラメータ
- Pydanticによるバリデーション

**同僚コード:** Tanakaさんが `services/etl.py` (ETL処理のコアロジック) を書き済み。あなたはこれをAPIとして公開するエンドポイントを作る。

**Claude Code用プロンプト:**
```
プロジェクト medical-data-api のStep 1を始めます。
Tanakaさん（同僚）が書いた services/etl.py を読んで、
それをFastAPIのエンドポイントとして公開するコードを app/routers/data.py に書きたい。
骨組み（関数名、ルート、型ヒントだけ）を見せて。中身のロジックは自分で書く。
```

---

### Step 2: Pytestでテスト自動化 (1時間)
**学べること:** ユニットテスト、テストフィクスチャ、テストカバレッジ

**概念キーワード:**
- ユニットテスト vs 統合テスト vs E2Eテスト
- テストフィクスチャ (pytest fixture)
- テストカバレッジ
- AAA パターン (Arrange, Act, Assert)
- モック (外部依存の切り離し)

**タスク:** Step 1で作ったAPIのテストを書く。TanakaさんのETL処理のテストも書く。

**Claude Code用プロンプト:**
```
Step 2: tests/test_data_router.py と tests/test_etl.py のテストを書きたい。
テストファイルの骨組み（テスト関数名、何をテストするかのコメント）だけ見せて。
assert文や具体的なロジックは自分で書く。
```

---

### Step 3: JWT認証の実装 (1.5時間)
**学べること:** 認証(Authentication) vs 認可(Authorization)、JWT、OAuth2

**概念キーワード:**
- 認証 (誰か？) vs 認可 (何ができるか？)
- JWT (JSON Web Token) の構造: Header.Payload.Signature
- アクセストークン vs リフレッシュトークン
- FastAPIの Depends() による依存性注入
- OAuth2PasswordBearer

**同僚コード:** Tanakaさんが `models/schemas.py` にユーザースキーマを追加済み。

**Claude Code用プロンプト:**
```
Step 3: JWT認証を実装したい。
app/auth/jwt_handler.py の骨組みを見せて。
- トークン生成関数
- トークン検証関数
- FastAPIの依存性注入で使うget_current_user関数
関数のシグネチャとdocstringだけ。中身は自分で書く。
```

---

### Step 4: マイクロサービス体験 + docker-compose (1.5時間)
**学べること:** マイクロサービスアーキテクチャ、サービス間通信、コンテナオーケストレーション

**概念キーワード:**
- マイクロサービス vs モノリス
- サービス間通信 (REST / gRPC / メッセージキュー)
- docker-compose による複数サービス管理
- サービスディスカバリ (コンテナ名でアクセス)
- API Gateway パターン

**同僚コード:** Suzukiさんが `notification-service/` (通知サービス) を作成済み。あなたのAPIからこの通知サービスを呼ぶ。

**Claude Code用プロンプト:**
```
Step 4: docker-compose.yml を書きたい。
構成:
- api (自分のFastAPIアプリ)
- notification (Suzukiさんの通知サービス)
- redis (キャッシュ用)
docker-compose.ymlの骨組み（サービス名とコメント）だけ見せて。
ポート設定、ボリューム、依存関係は自分で書く。
```

---

## 📅 Day 2（明日）

### Step 5: Dockerマルチステージビルド (1時間)
**学べること:** イメージサイズ最適化、ビルドステージ分離、本番用Docker構成

**概念キーワード:**
- シングルステージ vs マルチステージビルド
- ビルドステージ (依存インストール) → 実行ステージ (軽量イメージ)
- .dockerignore
- レイヤーキャッシュの活用

**同僚コード:** Suzukiさんがシングルステージの `Dockerfile.dev` を書いている。あなたは本番用 `Dockerfile` をマルチステージで書き直す。

**Claude Code用プロンプト:**
```
Step 5: 本番用のマルチステージDockerfileを書きたい。
Suzukiさんの Dockerfile.dev を参考に、本番用 Dockerfile の骨組みを見せて。
FROM文とステージ名、COMMENTだけ。COPY, RUN, CMD は自分で書く。
```

---

### Step 6: GitHub Actions CI/CD (1時間)
**学べること:** CI/CDパイプライン、自動テスト、自動デプロイ

**概念キーワード:**
- CI (Continuous Integration): コードの自動テスト
- CD (Continuous Delivery/Deployment): 自動デプロイ
- ワークフロー、ジョブ、ステップ
- トリガー (push, pull_request)
- シークレット管理

**Claude Code用プロンプト:**
```
Step 6: .github/workflows/ci.yml を書きたい。
やりたいこと:
- pushとPR時にトリガー
- Pythonセットアップ
- 依存インストール
- pytest実行
- lint (ruff)
YAMLの構造（ジョブ名とステップ名のコメント）だけ見せて。
コマンドは自分で書く。
```

---

### Step 7: ログ・監視の基礎 (45分)
**学べること:** 構造化ログ、ログレベル、監視の概念

**概念キーワード:**
- ログレベル (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- 構造化ログ (JSON形式)
- リクエストID (トレーサビリティ)
- Prometheus / Grafana (概念のみ)
- GCP Cloud Logging (概念のみ)

**同僚コード:** Suzukiさんが `middleware/logging_middleware.py` を途中まで書いている。あなたが仕上げる。

**Claude Code用プロンプト:**
```
Step 7: Suzukiさんのlogging_middleware.pyを仕上げたい。
まず構造化ログの設定ファイル app/core/logging_config.py の骨組みを見せて。
ロガーの設定とフォーマッターの枠だけ。設定値は自分で書く。
```

---

### Step 8: K8s / GCP 概念 + 高トラフィックAPI設計 (1時間)
**学べること:** Kubernetes基礎、GCPサービス、スケーリング戦略

**概念キーワード:**
- Pod / Service / Deployment / ReplicaSet
- GKE (Google Kubernetes Engine) vs Cloud Run
- 水平スケーリング vs 垂直スケーリング
- レートリミット
- キャッシュ戦略 (Redis)
- ロードバランシング

**タスク:** Redisキャッシュをアプリに組み込む（実装）+ K8sマニフェストを読む（概念理解）

**Claude Code用プロンプト:**
```
Step 8: Redisキャッシュを使ったAPI最適化をしたい。
app/core/cache.py の骨組みを見せて。
- Redis接続設定
- キャッシュget/set関数
- キャッシュデコレータ
関数シグネチャだけ。中身は自分で書く。

あと、Suzukiさんが書いたk8s/deployment.yamlを見せて。読み解きたい。
```

---

### Step 9: MLOps・推論API (45分)
**学べること:** モデルデプロイ、推論API、レイテンシ最適化

**概念キーワード:**
- モデルのシリアライズ (pickle, ONNX, TorchScript)
- 推論APIの設計
- バッチ推論
- モデル量子化
- A/Bテスト基盤

**タスク:** 簡単な分類モデルのAPIエンドポイントを作る。

**Claude Code用プロンプト:**
```
Step 9: 簡易的な推論APIを作りたい。
app/routers/prediction.py の骨組みを見せて。
- モデルロード関数
- 推論エンドポイント (/predict)
- バッチ推論エンドポイント (/predict/batch)
シグネチャとdocstringだけ。
```

---

### Step 10: 面談シミュレーション (1時間)
**タスク:** Antigravityで模擬面談。全Stepの技術について質問を受ける。

**Claude Code用プロンプト:** (使わない - Antigravityで実施)

---

## 📂 プロジェクト最終構成

```
medical-data-api/
├── app/
│   ├── __init__.py
│   ├── main.py                    ← FastAPIエントリポイント
│   ├── routers/
│   │   ├── data.py                ← [あなた] データAPIエンドポイント
│   │   └── prediction.py          ← [あなた] 推論API
│   ├── services/
│   │   ├── etl.py                 ← [Tanaka] ETLコア処理
│   │   └── notification_client.py ← [あなた] 通知サービス呼び出し
│   ├── auth/
│   │   └── jwt_handler.py         ← [あなた] JWT認証
│   ├── models/
│   │   └── schemas.py             ← [Tanaka] Pydanticスキーマ
│   ├── core/
│   │   ├── config.py              ← [Tanaka] 設定管理
│   │   ├── cache.py               ← [あなた] Redisキャッシュ
│   │   └── logging_config.py      ← [あなた] ログ設定
│   └── middleware/
│       └── logging_middleware.py   ← [Suzuki→あなた] ログミドルウェア
├── notification-service/
│   ├── main.py                    ← [Suzuki] 通知サービス
│   └── Dockerfile                 ← [Suzuki]
├── k8s/
│   └── deployment.yaml            ← [Suzuki] K8s定義（読み解き用）
├── tests/
│   ├── test_data_router.py        ← [あなた]
│   └── test_etl.py                ← [あなた]
├── Dockerfile                     ← [あなた] マルチステージビルド
├── Dockerfile.dev                 ← [Suzuki] 開発用
├── docker-compose.yml             ← [あなた]
├── .github/workflows/
│   └── ci.yml                     ← [あなた] CI/CD
├── pyproject.toml
└── README.md
```

---

## 💬 面談想定Q&A（各Stepで整理）

各Stepの後に「面談での答え方」テンプレートを用意。
形式:
```
Q: [想定質問]
A: [30秒で答えるテンプレート]
   - 概念の説明（1文）
   - 自分の経験に紐付け（1文）
   - なぜ重要か（1文）
```

---

## ⚡ クイックスタート

Step 1を始めるには、Antigravityで以下を送信:

**「Step 1 の概念説明をお願いします」**
