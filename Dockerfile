FROM debian:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev

RUN mkdir /srv/cartefede
RUN mkdir /var/log/cartefede

RUN touch /var/log/cartefede/access.log
RUN touch /var/log/cartefede/error.log

WORKDIR /srv/cartefede

COPY Models Models
COPY static static
COPY templates templates
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY dockerutils/cert.pem /etc/ssl/cartefede/certs/cert.pem
COPY dockerutils/key.pem /etc/ssl/cartefede/private/key.pem

RUN pip3 install -r requirements.txt --break-system-packages

EXPOSE 80 443

#create lowpriv user to run the app with low privileges
RUN useradd -ms /bin/bash lowpriv
RUN chown -R lowpriv:lowpriv /srv/cartefede
RUN chown -R lowpriv:lowpriv /var/log/cartefede
RUN chown -R lowpriv:lowpriv /etc/ssl/cartefede/

USER lowpriv

CMD ["gunicorn","-b","0.0.0.0:80","-w","3"]