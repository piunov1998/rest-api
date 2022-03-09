FROM python:3.10
WORKDIR /api
COPY requirements.txt .
COPY app.py /api
RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "app.py"]