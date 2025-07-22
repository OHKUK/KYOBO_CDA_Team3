FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv
COPY api_server.py .
COPY .env /app/.env
EXPOSE 5000
CMD ["python", "api_server.py"]
