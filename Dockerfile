# ---------------------------------------------
# 1. 베이스 이미지
# ---------------------------------------------

FROM python:3.10-slim AS base

# 파이썬 버퍼링 끄기 + pip 캐시 비활성

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 시스템 패키지 설치

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential gcc libpq-dev netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------
# 2. 파이썬 의존성 레이어
#       requirements.txt 가 바뀔 때만 캐시 무효화
# ---------------------------------------------

FROM base AS build

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


# ---------------------------------------------
# 3. 애플리케이션 레이어
# ---------------------------------------------

FROM build

# 시스템 -> 비루트 유저 생성
RUN adduser --disabled-password --gecos '' django
RUN mkdir -p /app/staticfiles && chown django:django /app/staticfiles
USER django

WORKDIR /app
COPY --chown=django:django . .

EXPOSE 8000

CMD ["bash", "-c", "echo 'Use docker-compose up' && sleep infinity"]