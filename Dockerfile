FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10-2020-04-27

RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev

WORKDIR /app
COPY app/requirements.txt ./

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

# =============================================
# Production settings
# =============================================
# COPY app/ ./
