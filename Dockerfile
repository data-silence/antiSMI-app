FROM python:3.11-slim

RUN mkdir /frontend

WORKDIR /frontend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

LABEL authors="data-silence"

RUN apt-get -y update && apt-get install -y mc curl

ENTRYPOINT ["streamlit", "run", "Power_news.py", "--server.port=8501", "--server.address=0.0.0.0"]