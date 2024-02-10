FROM python:3.11
USER root
RUN mkdir /Application
COPY . /Application/
WORKDIR /Application/
RUN pip install -r requirements.txt
RUN apt update -y && apt install awscli -y
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]