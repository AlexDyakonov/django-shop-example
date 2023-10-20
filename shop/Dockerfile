FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000


RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash shop && chmod 777 /opt /run

WORKDIR /shop

COPY --chown=shop:shop . .
RUN chown -R shop:shop /shop && chmod -R 755 /shop

RUN pip install -r requirements.txt

RUN pip install gunicorn

USER shop

CMD ["gunicorn","-b","0.0.0.0:8000","shop.wsgi:application"]