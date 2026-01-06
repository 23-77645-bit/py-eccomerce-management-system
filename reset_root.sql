UPDATE mysql.user SET authentication_string = '' WHERE User = 'root' AND Host = 'localhost';
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY '1234';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS ecommerce_db;
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'root'@'localhost' IDENTIFIED BY '1234';
FLUSH PRIVILEGES;