from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from subtrack.models import Notification, Subscription


class Command(BaseCommand):
    help = 'Send reminders for subscriptions due based on reminder_days_before.'

    def handle(self, *args, **options):
        count = 0
        for subscription in Subscription.objects.filter(is_active=True):
            if subscription.is_due_for_reminder():
                message = (
                    f'Reminder: {subscription.service_name} renews on '
                    f'{subscription.billing_date:%Y-%m-%d} for ${subscription.amount}.'
                )
                send_mail(
                    subject='SubTrack Billing Reminder',
                    message=message,
                    from_email='no-reply@subtrack.local',
                    recipient_list=[subscription.user.email or 'user@example.com'],
                    fail_silently=True,
                )
                Notification.objects.create(subscription=subscription, message=message)
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Sent {count} reminder(s).'))
