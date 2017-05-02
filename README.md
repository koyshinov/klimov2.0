Install mysql

	# apt-get install mysql-server
	# apt-get install mysql-client

Create database and user with name `klimov`

	$ mysql -u root -p
	mysql> CREATE DATABASE klimov;
	mysql> CREATE USER 'klimov'@'localhost' IDENTIFIED BY 'password';
	mysql> GRANT ALL PRIVILEGES ON klimov.* TO 'klimov'@'localhost';
	mysql> FLUSH PRIVILEGES;

Check connection with new mysql user
	
	$ mysql -u klimov -D klimov -p
	mysql> SHOW DATABASES;

Create all tables and first user with role admin
	
	mysql> [all queries in file create_db.sql]

Rewrite db settings in app/db_func.py:

	host = 'localhost',
        user = 'klimov',
	passwd = 'password'
	
Install others

	# apt-get install python3-pip
	# apt-get install python-mysqldb
	# pip3 install -r requirements.txt

