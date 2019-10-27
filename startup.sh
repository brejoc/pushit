#! /bin/bash

# Preparing directories for everything that is not static.
mkdir -p /var/www/pushit/db
mkdir -p /var/www/pushit/static-collection
mkdir -p /var/www/pushit/logs
mkdir -p /var/www/pushit/run
mkdir -p /var/www/pushit/backup

# Collecting all of static files. Destination folder is defined in local_settings.py.
/var/www/pushit/sandbox/bin/python3 /var/www/pushit/manage.py collectstatic --noinput

# Create backup and apply migrations
echo "#####################################"
echo "#       database migrations         #"
echo "#####################################"
if [ -f "/var/www/pushit/db/production.sqlite3" ]; then
  cp /var/www/pushit/db/production.sqlite3 /var/www/pushit/backup/production.sqlite3.$(date +%s)
fi
/var/www/pushit/sandbox/bin/python3 /var/www/pushit/manage.py migrate

# PID file might have stalled. Deleting it.
rm -f /var/www/pushit/run/gunicorn.pid

# Starting Gunicorn.
/var/www/pushit/sandbox/bin/gunicorn \
    -c /var/www/pushit/gunicorn.conf.py \
    -p /var/www/pushit/run/gunicorn.pid \
    pushit.wsgi:application
