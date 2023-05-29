FROM tiangolo/uvicorn-gunicorn:python3.11-slim

WORKDIR /app
COPY app/requirements.txt ./

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

# =============================================
# Production settings
# =============================================
# COPY app/ ./
