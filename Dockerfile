# Parent image
FROM python:3.7.0-slim

# Working directory
WORKDIR /src

# Asenna riippuvuudet
COPY requirements.txt /src
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Kopioi tarvittavat tiedostot src:n alle
COPY src /src
COPY markku.sql /src
COPY .env /src

# Aja markku, kun container käynnistetään
CMD ["python", "markku.py"]
