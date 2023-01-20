FROM python:3.10-alpine

WORKDIR /app
ADD ./backend/requirements.txt /app/backend/

RUN pip install --upgrade pip && pip install -r backend/requirements.txt

ADD ./docker /app/docker
ADD ./backend /app/backend

RUN chmod +x /app/docker/parser/parser-entrypoint.sh && chmod +x /app/backend/manage.py