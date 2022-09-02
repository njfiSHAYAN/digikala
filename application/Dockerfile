FROM python:3.9

WORKDIR /app

ENV CONFIG_ADDR "application/config.json"

COPY requirements.txt .

RUN pip install -r requirements.txt && mkdir application

COPY . ./application

CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "80"]


