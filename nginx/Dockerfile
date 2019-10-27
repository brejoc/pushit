FROM registry.access.redhat.com/ubi8/ubi

LABEL MAINTAINER="brejoc@gmail.com"

# Volume for variable files
VOLUME [ "/var/www/pushit/logs", "/var/www/pushit/run", "/var/www/pushit/static-collection" ]

# Install Nginx
RUN dnf install nginx -y

COPY ./pushit.brejoc.com.conf /etc/nginx/conf.d

ENTRYPOINT [ "nginx",  "-g", "daemon off;" ]
EXPOSE 81
