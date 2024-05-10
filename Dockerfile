FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

EXPOSE 8000

CMD ["sh", "-c", "uvicorn fastapi_backend:app --host 0.0.0.0 --port 8000 & streamlit run --server.port 8501 streamlit_frontend.py"]
