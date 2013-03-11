.PHONY: run rebuilddb reset_fuss

SHELL=/bin/bash

run:
	./manage.py runserver

rebuilddb:
	rm ./sqlite3_akafun.db; ./manage.py syncdb

reset_fuss:
	./manage.py reset fuss

rfuss: reset_fuss run
