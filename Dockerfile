FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install first (better layer caching)
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Now copy the cleaned source code
COPY ./app /app

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
