FROM python:3

WORKDIR /api-server
COPY . /api-server
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000
CMD ["python3", "run.py"]
