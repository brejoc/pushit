from datetime import date
from datetime import timedelta

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


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


@receiver(pre_save, sender=Event)
def my_callback(sender, instance, *args, **kwargs):
    """\
    With this nasty hack we convert seconds in minutes.
    """
    instance.duration = timedelta(minutes=instance.duration.seconds)


