from python:3.7.12-alpine3.15

WORKDIR /usr/src/app

RUN apk add --update musl-dev gcc libffi-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main ./main
COPY test ./test
COPY prod-waitress.py ./

EXPOSE 8887

CMD [ "python", "./prod-waitress.py" ]