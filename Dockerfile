FROM python:3.11

WORKDIR /app

COPY main.py /app/
COPY book.json /app/

ENV PYTHONIOENCODING=utf-8

CMD ["python", "main.py"]