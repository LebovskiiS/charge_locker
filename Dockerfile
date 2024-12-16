FROM python:3.11-slim


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

EXPOSE 4000

CMD ["python", "main.py"]