FROM python:3.11.3

RUN mkdir -p ./bot
WORKDIR ./bot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]