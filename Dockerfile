FROM python:3.9

WORKDIR /app
COPY . /app
RUN pip install -r ./src/requirements.txt
CMD ["python", "src/main.py"]