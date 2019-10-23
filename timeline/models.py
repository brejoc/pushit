from datetime import date
from datetime import timedelta

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver

from webpush import send_user_notification


class Event(models.Model):
    """\
    Events are the things shown in the timeline.
    """
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE, verbose_name='Aktivität')
    date = models.IntegerField(choices=((1, "Heute"),
                                        (2, "Gestern"),
                                        (3, "Vorestern")),
                                default=1,
                                verbose_name="Datum")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Benutzer')
    duration = models.DurationField(default="30", verbose_name='Dauer (in Minuten)')
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung (optional)")
    # auto updated fields below
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def real_date(self):
        return self.created_at.date() - timedelta(days=self.date-1)

    def __str__(self):
        return self.activity.name


class Activity(models.Model):
    """\
    Activities the user can choose from.
    """
    name = models.CharField(max_length=50, verbose_name='Name')
    # auto updated fields below
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['activity', 'duration', 'date', 'description']


@receiver(post_save, sender=Event)
def send_web_notifications(sender, instance, *args, **kwargs):
    """\
    Sending notifications after adding Activities.
    """
    payload = {"head": "Neue Aktivität von {}".format(instance.user),
               "body": "{} für {}".format(instance.activity, instance.duration)}
    for user in User.objects.all():
        if user != instance.user:
            send_user_notification(user=user, payload=payload, ttl=1000)

@receiver(pre_save, sender=Event)
def fix_duration(sender, instance, *args, **kwargs):
    """\
    With this nasty hack we convert seconds in minutes.
    """
    instance.duration = timedelta(minutes=instance.duration.seconds)
