"""This module defines functions for sending email on Dag task success and failure"""
from airflow.utils.email import send_email

from config.config import ADMIN_EMAIL

def success_email(context):
    """This function send an email in case of success DAG task"""
    task_instance = context['task_instance']
    task_status = 'Success'
    subject = f'🎉 Airflow Task {task_instance.task_id} - {task_status} 🎉'
    body = (
        f"<h3 style='color: green;'>🎉 Airflow Task Notification 🎉</h3>"
        f"<p><strong>Task ID:</strong> {task_instance.task_id}</p>"
        f"<p><strong>Status:</strong> <span style='color: green;'>{task_status}</span></p>"
        f"<p><strong>Execution Date(UTC):</strong> {context['data_interval_start']}</p>"
        f"<p>Dear User,</p>"
        f"<p>We are pleased to inform you that the task <strong>{task_instance.task_id}\
        </strong> has completed successfully. ✅</p>"
        f"<p>For more details, please refer to the \
        <a href='{task_instance.log_url}'>task log</a>.</p>"
        f"<p>Best regards,<br><span style='color: blue;'>Big Data News Recommender</span></p>"
    )
    to_email = ADMIN_EMAIL # Recipient email

    send_email(
        to=to_email,
        subject=subject,
        html_content=body,
        conn_id='smtp_default'
        #conn_id='smtp-connection'  # Ensure this matches your Airflow SMTP connection ID
    )

def failure_email(context):
    """This function send an email in case of failed DAG task"""
    task_instance = context['task_instance']
    task_status = 'Failed'
    subject = f'⚠️ Airflow Task {task_instance.task_id} - {task_status} ⚠️'
    body = (
        f"<h3 style='color: red;'>⚠️ Airflow Task Notification ⚠️</h3>"
        f"<p><strong>Task ID:</strong> {task_instance.task_id}</p>"
        f"<p><strong>Status:</strong> <span style='color: red;'>{task_status}</span></p>"
        f"<p><strong>Execution Date(UTC):</strong> {context['data_interval_start']}</p>"
        f"<p>Dear User,</p>"
        f"<p>We regret to inform you that the task \
        <strong>{task_instance.task_id}</strong> has failed. ❌</p>"
        f"<p>Please review the \
        <a href='{task_instance.log_url}'>task log</a> \
        for more details and take necessary actions.</p>"
        f"<p>Best regards,<br><span style='color: blue;'>Big Data News Recommender</span></p>"
    )
    to_email = ADMIN_EMAIL  # Recipient email

    send_email(
        to=to_email,
        subject=subject,
        html_content=body,
        conn_id='smtp_default'  # Ensure this matches your Airflow SMTP connection ID
        #conn_id='smtp-connection'
    )
