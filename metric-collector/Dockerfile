FROM python:3

WORKDIR /metric-collector
COPY . /metric-collector
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7770
CMD ["python3", "run.py"]
