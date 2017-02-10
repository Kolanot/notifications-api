from datetime import datetime
import uuid

from app.models import User, Template, Notification, SMS_TYPE, KEY_TYPE_NORMAL
from app.dao.users_dao import save_model_user
from app.dao.notifications_dao import dao_create_notification
from app.dao.templates_dao import dao_create_template


def create_user(mobile_number="+447700900986", email="notify@digital.cabinet-office.gov.uk"):
    data = {
        'name': 'Test User',
        'email_address': email,
        'password': 'password',
        'mobile_number': mobile_number,
        'state': 'active'
    }
    user = User.query.filter_by(email_address=email).first()
    if not user:
        user = User(**data)
    save_model_user(user)
    return user


def create_template(service, user=None, template_type=SMS_TYPE):
    data = {
        'name': '{} Template Name'.format(template_type),
        'template_type': template_type,
        'content': 'Dear Sir/Madam, Hello. Yours Truly, The Government.',
        'service': service,
        'created_by': service.created_by,
    }
    if template_type != SMS_TYPE:
        data['subject'] = 'Template subject'
    template = Template(**data)
    dao_create_template(template)
    return template


def create_notification(
    template,
    job=None,
    job_row_number=None,
    to_field='+447700900855',
    status='created',
    reference=None,
    created_at=None,
    sent_at=None,
    billable_units=1,
    personalisation=None,
    api_key_id=None,
    key_type=KEY_TYPE_NORMAL,
    sent_by=None,
    client_reference=None
):
    if created_at is None:
        created_at = datetime.utcnow()
    data = {
        'id': uuid.uuid4(),
        'to': to_field,
        'job_id': job.id if job else None,
        'job': job,
        'service_id': template.service_id,
        'template_id': template.id if template else None,
        'template': template,
        'template_version': template.version,
        'status': status,
        'reference': reference,
        'created_at': created_at,
        'sent_at': sent_at,
        'billable_units': billable_units,
        'personalisation': personalisation,
        'notification_type': template.template_type,
        'api_key_id': api_key_id,
        'key_type': key_type,
        'sent_by': sent_by,
        'updated_at': None,
        'client_reference': client_reference,
        'job_row_number': None
    }
    notification = Notification(**data)
    dao_create_notification(notification)
    return notification