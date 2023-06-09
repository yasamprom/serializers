FROM python:3.9
RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app/serializers"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]