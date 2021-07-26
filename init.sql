create user administrator with password 'admin123';
alter role administrator set client_encoding to 'utf8';
alter role administrator set default_transaction_isolation to 'read committed';
alter role administrator set timezone to 'UTC';
ALTER USER administrator CREATEDB;
create database crm owner administrator;