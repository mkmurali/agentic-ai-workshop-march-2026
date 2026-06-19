FROM python:3.12-slim

WORKDIR /app

COPY workshop/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn

# Create a non-root user to run the application
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY workshop/ ./workshop/

# Transfer ownership to non-root user
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

CMD ["uvicorn", "workshop.module_06_deploy.app_fastapi:app", "--host", "0.0.0.0", "--port", "8080"]
