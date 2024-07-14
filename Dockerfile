FROM python:3.12

ENV DJANGO_SETTINGS_MODULE=src.settings.prod
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY ./requirements ./requirements
ADD ./src ./src
ADD ./manage.py ./

RUN pip install --upgrade pip
RUN pip install -r requirements/base.txt


EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.wsgi:application"]