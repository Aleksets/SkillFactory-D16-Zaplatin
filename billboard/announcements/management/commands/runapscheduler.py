from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from ...models import Announcement

import logging
import re

logger = logging.getLogger(__name__)


def weekly_emails_job():
    # Job processing logic here...
    last_week = timezone.now() - timezone.timedelta(7)
    announcements = Announcement.objects.filter(add_date__gte=last_week)
    for user in User.objects.all():
        html_content = render_to_string(
            'week_announcements_email.html',
            {
                'user': user,
                'announcements': announcements,
                'link': f'{settings.SITE_URL}/announcements/',
            }
        )
        msg = EmailMultiAlternatives(
            subject='Last week announcements list',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_emails_job,
            trigger=CronTrigger(day_of_week="mon", hour="05", minute="00"),
            id="weekly_emails_job",  # unique id
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_emails_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
