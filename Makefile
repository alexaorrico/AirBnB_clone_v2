test:
	python -m unittest discover -v
	HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd \
	HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db \
	HBNB_TYPE_STORAGE=db python3 -m unittest discover tests

test-fs:
	python -m unittest \
	discover -v

test-db:
	HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd \
	HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db \
	HBNB_TYPE_STORAGE=db python3 -m unittest discover tests

setup-db-test:
	cat setup_mysql_test.sql | mysql -uroot -p

setup-db-dev:
	cat setup_mysql_dev.sql | mysql -uroot -p
