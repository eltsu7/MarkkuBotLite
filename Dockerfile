# Parent image
FROM python:3.7.0-slim

# Asenna riippuvuudet
COPY requirements.txt /src
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Kopioi tarvittavat tiedostot src:n alle
COPY . /

# Aja markku, kun container käynnistetään
CMD ["python", "markku.py"]
