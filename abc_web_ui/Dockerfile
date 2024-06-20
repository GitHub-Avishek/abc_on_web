FROM python:latest

WORKDIR /app

COPY ./app_code ./code

COPY ./.streamlit ./.streamlit

COPY ./requirememts.txt ./requirememts.txt

RUN pip install -r ./requirememts.txt
