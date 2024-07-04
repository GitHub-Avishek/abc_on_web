FROM python:latest

WORKDIR /app

COPY ./app_code ./gui_code

COPY ./.streamlit ./.streamlit

COPY ./requirememts.txt ./gui_code/requirememts.txt

RUN pip install -r ./gui_code/requirememts.txt
