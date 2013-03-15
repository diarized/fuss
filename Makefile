.PHONY: run rebuilddb reset_fuss

SHELL=/bin/bash

run:
	./manage.py runserver

rebuilddb:
	rm ./sqlite3_akafun.db; ./manage.py syncdb

reset_fuss:
	./manage.py reset fuss

bgwsgi:
	./manage.py runwsgiserver host=0.0.0.0 server_name=krk-lpf90 daemonize=True pidfile=/home/artur/fun/fuss/wsgi.pid

fgwsgi:
	./manage.py runwsgiserver host=0.0.0.0 server_name=krk-lpf90

rfuss: reset_fuss fgwsgi

fuckit: rebuilddb fgwsgi

