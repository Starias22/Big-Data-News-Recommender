#!/bin/bash

# Read secrets for Airflow user creation
if [ -f /run/secrets/airflow_user ]; then
    AIRFLOW_USER=$(cat /run/secrets/airflow_user)
fi

if [ -f /run/secrets/airflow_email ]; then
    AIRFLOW_EMAIL=$(cat /run/secrets/airflow_email)
fi

if [ -f /run/secrets/airflow_password ]; then
    AIRFLOW_PASSWORD=$(cat /run/secrets/airflow_password)
fi

if [ -f /run/secrets/airflow_firstname ]; then
    AIRFLOW_FIRSTNAME=$(cat /run/secrets/airflow_firstname)
fi

if [ -f /run/secrets/airflow_lastname ]; then
    AIRFLOW_LASTNAME=$(cat /run/secrets/airflow_lastname)
fi

# Perform Airflow database migration
airflow db migrate

# Create Airflow user using the secrets
airflow users create \
    --username "$AIRFLOW_USER" \
    --firstname "$AIRFLOW_FIRSTNAME" \
    --lastname "$AIRFLOW_LASTNAME" \
    --role "Admin" \
    --email "$AIRFLOW_EMAIL" \
    --password "$AIRFLOW_PASSWORD"

# Continue with other commands (like starting the webserver)
#exec "$@"
