test:
	python3 -m unittest discover -v
	HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd \
	HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db \
	HBNB_TYPE_STORAGE=db python3 -m unittest discover tests

test-fs:
	python3 -m unittest \
	discover -v

test-api:
	HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost \
	HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 \
	HBNB_API_PORT=5000 python3 -m api.v1.app

test-db:
	HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd \
	HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db \
	HBNB_TYPE_STORAGE=db python3 -m unittest discover tests

test-task-5:
	HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd \
	HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db HBNB_TYPE_STORAGE=db \
	python3 ./test_task_5.py

setup-db-test:
	cat setup_mysql_test.sql | mysql -uroot -p

setup-db-dev:
	cat setup_mysql_dev.sql | mysql -uroot -p
