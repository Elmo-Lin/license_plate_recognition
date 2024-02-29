FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app

RUN pip install Flask opencv-python-headless pytesseract

RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean


CMD ["flask", "run", "--host=0.0.0.0"]
