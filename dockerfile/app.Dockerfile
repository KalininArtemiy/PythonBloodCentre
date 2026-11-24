FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN  playwright install --with-deps firefox
COPY . .

EXPOSE 8000

CMD ["python", "-m", "app.main"]
