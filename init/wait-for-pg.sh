#!/bin/sh
# wait-for-postgres.sh

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "psql" -U "ops" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
  
>&2 echo "Postgres is up - executing command"