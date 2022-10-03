CREATE DATABASE IF NOT EXISTS ntmirror_test;
GRANT USAGE ON *.* to 'myuser'@localhost identified by 'mypass';
GRANT ALL PRIVILEGES ON `ntmirror_test`.* to 'myuser'@localhost;
FLUSH PRIVILEGES;
