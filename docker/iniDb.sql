create
user file_user with password 'pswd';

grant all privileges on database
file_database to file_user;

grant all privileges on all
tables in schema public to file_user;

grant all privileges on all
sequences in schema public to file_user;