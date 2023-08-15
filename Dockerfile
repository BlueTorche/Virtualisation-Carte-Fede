FROM debian:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev

RUN mkdir /srv/healthapp
RUN mkdir /var/log/healthapp

RUN touch /var/log/healthapp/access.log
RUN touch /var/log/healthapp/error.log

WORKDIR /srv/healthapp

COPY Models Models
COPY static static
COPY templates templates
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY dockerutils/cert.pem /etc/ssl/healthapp/certs/cert.pem
COPY dockerutils/key.pem /etc/ssl/healthapp/private/key.pem

RUN pip3 install -r requirements.txt --break-system-packages

EXPOSE 8000 4343

#create lowpriv user to run the app with low privileges
RUN useradd -ms /bin/bash lowpriv
RUN chown -R lowpriv:lowpriv /srv/healthapp
RUN chown -R lowpriv:lowpriv /var/log/healthapp
RUN chown -R lowpriv:lowpriv /etc/ssl/healthapp/

USER lowpriv

CMD ["gunicorn","-b","0.0.0.0:4343","-w","3","--certfile","/etc/ssl/healthapp/certs/cert.pem","--keyfile","/etc/ssl/healthapp/private/key.pem","app:create_app()"]