FROM python:3.6-slim
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "main.py"]