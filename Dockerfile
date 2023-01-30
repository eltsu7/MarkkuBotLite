# Parent image
FROM python:3.9-slim

COPY . /
RUN pip install --upgrade pip --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "markku.py"]
