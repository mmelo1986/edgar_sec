FROM mysql:latest

COPY /scripts/create_db.sql /docker-entrypoint-initdb.d/create_db.sql
# RUN mysql -u root < create_db.sql

EXPOSE 3306