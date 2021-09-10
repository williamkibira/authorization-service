FROM python:3.9.6-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends g++ python3-dev bash curl libpq-dev

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -lah .
EXPOSE 4000
ENTRYPOINT ["sh","run.sh"]
