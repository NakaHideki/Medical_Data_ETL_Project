# ========== ステージ1: ビルド用 ==========
FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ========== ステージ2: 本番用（軽量） ==========
FROM python:3.9-slim AS production

WORKDIR /app

# ビルドステージからライブラリだけコピー（ビルドツールは含まない）
COPY --from=builder /install /usr/local

COPY . .

# 本番用の設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
