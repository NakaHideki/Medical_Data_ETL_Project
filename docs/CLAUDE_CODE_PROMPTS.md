# 🤖 Claude Code用プロンプト集

このファイルをClaude Codeで開いて、各Stepのプロンプトをコピペして使ってください。

---

## Step 1: FastAPIでREST API設計

### プロンプト1: 骨組みの取得
```
このプロジェクトのStep 1を始めます。
app/services/etl.py (Tanakaさんが書いた) を読んで理解してください。

その上で app/routers/data.py の骨組みだけ作ってください。
条件:
- FastAPIのルーター使用
- 以下のエンドポイントを定義:
  - POST /upload : CSVファイルアップロード＋バリデーション
  - POST /process : データクレンジング処理
  - POST /transform : DHCS提出用フォーマット変換
  - GET /summary : データサマリー取得
- 関数のシグネチャ、型ヒント、docstringだけ書く
- ロジック部分は # TODO: 実装してください とコメントのみ
- app/models/schemas.py のスキーマを使う
```

### プロンプト2: レビュー依頼
```
app/routers/data.py を自分で実装しました。
コードレビューをお願いします。
以下の観点で見てください:
- RESTful設計として適切か
- エラーハンドリングは十分か
- Tanakaさんの etl.py との連携は正しいか
- 型ヒントは適切か
改善点があれば具体的に教えてください。
```

---

## Step 2: Pytestでテスト自動化

### プロンプト1: 骨組みの取得
```
Step 2: テストを書きます。
tests/test_data_router.py と tests/test_etl.py の骨組みを作ってください。
条件:
- pytest + pytest-asyncio 使用
- FastAPIのTestClient使用
- 各エンドポイントに最低2つのテストケース（正常系・異常系）
- テスト関数名、docstring、# TODO: assert文を書いてください のコメントだけ
- conftest.py にフィクスチャも骨組みだけ
```

### プロンプト2: レビュー依頼
```
テストコードを実装しました。
レビューと実行をお願いします。
pytest --cov=app -v で実行してカバレッジも確認してください。
テストが落ちる場合は原因だけ教えて、修正は自分でやります。
```

---

## Step 3: JWT認証の実装

### プロンプト1: 骨組みの取得
```
Step 3: JWT認証を実装します。
app/auth/jwt_handler.py の骨組みを作ってください。
条件:
- python-jose を使用
- app/core/config.py の設定を使う
- app/models/schemas.py の TokenData, TokenPayload を使う
- 以下の関数の骨組み:
  - create_access_token(data: dict) -> str
  - verify_token(token: str) -> TokenPayload
  - get_current_user(token: str = Depends(...)) -> dict
- 関数シグネチャとdocstringだけ。ロジックは TODO
```

### プロンプト2: 統合確認
```
JWT認証を実装しました。
app/routers/data.py のエンドポイントに認証を適用してください。
具体的には:
- /upload, /process, /transform は認証必須
- /summary と /health は認証不要
適用方法のヒントだけください（Depends の使い方）。実装は自分でやります。
```

---

## Step 4: マイクロサービス体験 + docker-compose

### プロンプト1: 通知クライアント骨組み
```
Step 4: マイクロサービス間通信を実装します。
notification-service/main.py (Suzukiさんが書いた) を読んでください。

app/services/notification_client.py の骨組みを作ってください。
条件:
- httpx を使って通知サービスを呼び出す非同期クライアント
- 関数: send_notification(event_type, message, metadata=None)
- エラーハンドリング（通知サービスが落ちていても本体APIは動く）
- シグネチャとdocstringだけ
```

### プロンプト2: docker-compose骨組み
```
docker-compose.yml の骨組みを作ってください。
サービス構成:
- api: 自分のFastAPIアプリ (port 8000)
- notification: Suzukiさんの通知サービス (port 8001)
- redis: キャッシュ用
各サービスの service名とコメントだけ。
ports, volumes, depends_on, environment は自分で書きます。
```

---

## Step 5: Dockerマルチステージビルド

### プロンプト1: 骨組みの取得
```
Step 5: 本番用Dockerfileをマルチステージで書きます。
Dockerfile.dev (Suzukiさんが書いた) を見てください。

本番用 Dockerfile の骨組みを作ってください。
条件:
- ステージ1: builder (依存インストール)
- ステージ2: runtime (本番実行用、軽量)
- FROM文とステージ名、各ステージの目的コメントだけ
- COPY, RUN, CMD は TODO
```

---

## Step 6: GitHub Actions CI/CD

### プロンプト1: 骨組みの取得
```
Step 6: CI/CDパイプラインを作ります。
.github/workflows/ci.yml の骨組みを作ってください。
条件:
- トリガー: push (main), pull_request
- ジョブ: lint, test, build
- 各ステップの name だけ書いて、run は TODO
```

---

## Step 7: ログ・監視の基礎

### プロンプト1: ログ設定の骨組み
```
Step 7: 構造化ログを設定します。
app/core/logging_config.py の骨組みを作ってください。
条件:
- Python標準のloggingモジュール使用
- JSON形式出力（Cloud Logging互換）
- 関数: setup_logging() の骨組み
```

### プロンプト2: ミドルウェア仕上げ
```
app/middleware/logging_middleware.py を見てください。
Suzukiさんが途中まで書いています。
TODOの部分を実装するヒント（各TODOで使うべきモジュール/関数名）だけ教えてください。
実装は自分でやります。
```

---

## Step 8: Redis キャッシュ + K8s概念理解

### プロンプト1: キャッシュの骨組み
```
Step 8: Redisキャッシュを実装します。
app/core/cache.py の骨組みを作ってください。
条件:
- redis-py (async) 使用
- get_cache / set_cache / delete_cache 関数
- キャッシュデコレータ (cache_response)
- シグネチャとdocstringだけ
```

### プロンプト2: K8s読み解き
```
k8s/deployment.yaml (Suzukiさんが書いた) を読んでください。
以下を教えてください:
1. このファイルに定義されているK8sリソースの一覧
2. 各リソースが何をしているか1行で
3. 面談で「K8sの経験は？」と聞かれた時に答えられるポイント
```

---

## Step 9: MLOps・推論API

### プロンプト1: 骨組みの取得
```
Step 9: 簡易推論APIを作ります。
app/routers/prediction.py の骨組みを作ってください。
条件:
- scikit-learn の簡易モデル（IsolationForest等）で医療費の異常検知
- POST /predict : 単一レコードの異常検知
- POST /predict/batch : バッチ推論
- GET /model/info : モデル情報
- シグネチャとdocstringだけ
```

---

## 汎用プロンプト

### 「分からない」時
```
[ファイル名] の [関数名/行番号] が分かりません。
初心者向けに、この部分が何をしているか説明してください。
ただしコードは書かないでください。概念だけ教えてください。
```

### テスト実行
```
pytest tests/ -v --tb=short で全テストを実行してください。
失敗したテストがあれば、原因のヒントだけください。修正は自分でやります。
```

### 全体動作確認
```
uvicorn app.main:app --reload で起動して、
curl で /health, /api/v1/upload 等を叩いて動作確認してください。
エラーが出たら原因のヒントだけください。
```
