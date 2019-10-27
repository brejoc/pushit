FROM registry.access.redhat.com/ubi8/ubi

LABEL MAINTAINER="brejoc@gmail.com"

# Volume for variable files
VOLUME [ "/home/web/pushit/db", "/home/web/pushit/static-collection", "/home/web/pushit/logs", "/home/web/pushit/run", "/home/web/pushit/backup" ]

# Expose the port where gunicorn is listening on
EXPOSE 8000/tcp

# Add the sources and delete sandbox
ADD . /var/www/pushit
RUN rm -rf /var/www/pushit/sandbox

# Create virtualenv and install requirements
RUN dnf install python3-virtualenv -y
RUN virtualenv-3 /var/www/pushit/sandbox
RUN /var/www/pushit/sandbox/bin/pip install -r /var/www/pushit/requirements_production.txt


WORKDIR /var/www/pushit/
ENTRYPOINT [ "/var/www/pushit/startup.sh" ]
