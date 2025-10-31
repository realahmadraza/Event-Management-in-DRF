from celeryy import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Event


@shared_task
def send_event_reminder(event_id):
    try:
        event = Event.objects.get(pk=event_id)
        subject = f"Reminder: {event.title}"
        message = f"Your event {event.title} starts at {event.start_time}"
        recipients = [u.email for u in event.invited.all() if u.email]
        if recipients:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
            return True
    except Event.DoesNotExist:
        return False
    return False