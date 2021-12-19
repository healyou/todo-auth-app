from python:3.7.12-alpine3.15

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/log
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main ./main
COPY test ./test
COPY prod-waitress.py ./

EXPOSE 8887
VOLUME /usr/src/app/log

CMD [ "python", "./prod-waitress.py" ]