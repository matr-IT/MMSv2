from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mail_management_service.models import Mailing, MailingAttempt


def send_mailing(mailing_id):
    try:
        mailing = Mailing.objects.get(pk=mailing_id)
    except Mailing.DoesNotExist:
        raise ValueError(f"Рассылка с id={mailing_id} не найдена.")

    now = timezone.now()
    if mailing.disabled:
        raise ValueError("Рассылка отключена; отправка запрещена.")
    if not (mailing.start_time <= now < mailing.end_time):
        raise ValueError("Отправка не разрешена: текущее время вне окна рассылки.")

    mailing.status = "in_progress"
    mailing.save(update_fields="status")

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    if not from_email:
        from_email = ""

    success_count = 0
    fail_count = 0

    recipients = mailing.recipients.all()
    subject = mailing.message.subject
    body = mailing.message.body

    for recipient in recipients:
        try:
            sent = send_mail(subject, body, from_email, [recipient.email])
            if sent:
                status = "success"
                server_response = ""
                success_count += 1
            else:
                status = "failed"
                server_response = "send_mail вернул 0"
                fail_count += 1
        except Exception as e:
            status = "failed"
            server_response = str(e)
            fail_count += 1

        MailingAttempt.objects.create(
            mailing=mailing,
            status=status,
            server_response=server_response,
        )

    return {
        "success_count": success_count,
        "fail_count": fail_count,
        "total": len(recipients),
    }
