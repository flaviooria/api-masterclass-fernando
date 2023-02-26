FROM python:3.10.10-alpine3.17

ARG URL_MYSQL

WORKDIR /home/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . ./

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

