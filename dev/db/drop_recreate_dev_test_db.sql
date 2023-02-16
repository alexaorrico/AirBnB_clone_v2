-- creates MySQL database hbnb_test_db only if not existing
-- and gives privileges to user hbnb_test on 2 DB's
DROP DATABASE IF EXISTS hbnb_test_db;
DROP DATABASE IF EXISTS hbnb_dev_db;
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
GRANT ALL PRIVILEGES ON hbnb_dev_db.*
      TO hbnb_dev@localhost
      IDENTIFIED BY 'hbnb_dev_pwd';
GRANT SELECT ON performance_schema.*
      TO hbnb_dev@localhost
      IDENTIFIED BY 'hbnb_dev_pwd';
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
GRANT ALL PRIVILEGES ON hbnb_test_db.*
      TO hbnb_test@localhost
      IDENTIFIED BY 'hbnb_test_pwd';
GRANT SELECT ON performance_schema.*
      TO hbnb_test@localhost
      IDENTIFIED BY 'hbnb_test_pwd';
