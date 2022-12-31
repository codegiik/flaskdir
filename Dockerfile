FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip3 install poetry 

RUN poetry install

RUN poetry build

WORKDIR /app/dist

RUN mkdir output
RUN tar -xf *.tar.gz -C output --strip-components=1

FROM python:3.10-slim

WORKDIR /app

COPY --from=0 /app/dist/output .

RUN python3 setup.py install

EXPOSE 8000

CMD ["serve"]
