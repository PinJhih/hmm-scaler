FROM python:3

WORKDIR /scaling-detector
COPY . /scaling-detector
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7700
CMD ["python3", "run.py"]
