FROM python:3.12-slim
WORKDIR /
RUN apt-get update && apt-get install -y libpq-dev gcc
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
