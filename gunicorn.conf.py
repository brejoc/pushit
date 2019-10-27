from __future__ import unicode_literals
import multiprocessing

bind = "unix:/var/www/pushit/run/gunicorn.sock"
workers = 4
errorlog = "/var/www/pushit/logs/gunicorn_error.log"
loglevel = "error"
proc_name = "pushit.brejoc.com"
