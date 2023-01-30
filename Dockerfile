# Parent image
FROM python:3.7.0-slim

COPY . /
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "markku.py"]
