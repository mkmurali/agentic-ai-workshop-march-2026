FROM python:3.12-slim

WORKDIR /app

COPY workshop/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn

COPY workshop/ ./workshop/

EXPOSE 8080

CMD ["uvicorn", "workshop.module_06_deploy.app_fastapi:app", "--host", "0.0.0.0", "--port", "8080"]
