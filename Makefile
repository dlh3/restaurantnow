reset:
	sudo rm -rf database/
	sudo mkdir -p database
	sudo chmod 777 database
	python manage.py syncdb --noinput
	sudo chmod 777 database/*
	sudo cat sqlData.sql | sqlite3 database/restaurantnow.sqlite
