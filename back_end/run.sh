#/bin/bash

export MYSQL_DB_INSTANCE="<REMPLACEZ>"
export MYSQL_DATABASE="<REMPLACEZ>"
export MYSQL_USER="<REMPLACEZ>"
export MYSQL_PASSWORD="<REMPLACEZ>"
export FLASK_APP=back_end/webserver
export FLASK_DEBUG=True
flask run
