FROM python:3.9-slim-buster
RUN pip3 install flask flask-wtf email_validator requests flask-login flask sqlalchemy
COPY app.py app.py
CMD python app.py