FROM python:3.12

RUN mkdir /main_app

WORKDIR /main_app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chmod=+x ./docker/app.sh ./docker/app.sh

ENTRYPOINT ["./docker/app.sh"]

COPY . .