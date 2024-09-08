#!/bin/bash

# Read secrets and export as environment variables
if [ -f /run/secrets/smtp_user ]; then
    export AIRFLOW__SMTP__SMTP_USER=$(cat /run/secrets/smtp_user)
fi

if [ -f /run/secrets/smtp_password ]; then
    export AIRFLOW__SMTP__SMTP_PASSWORD=$(cat /run/secrets/smtp_password)
fi

if [ -f /run/secrets/smtp_mail_from ]; then
    export AIRFLOW__SMTP__SMTP_MAIL_FROM=$(cat /run/secrets/smtp_mail_from)
fi

# Start Airflow
exec airflow "$@"
