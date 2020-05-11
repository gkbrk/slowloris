FROM python:3.8-alpine

LABEL maintainer="Amin Vakil <info@aminvakil.com>"

RUN pip install --no-cache-dir slowloris PySocks --upgrade

ENTRYPOINT ["slowloris"]
