from datetime import timedelta

from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels

# Create your models here.


class Room(models.Model):
    users = models.ManyToManyField("accounts.Profile", related_name="rooms")
    created_date = jmodels.jDateTimeField(auto_now_add=True)
    updated_date = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f"room: {self.pk}"

    class Meta:
        ordering = ["-created_date", '-updated_date']


class Message(models.Model):
    author = models.ForeignKey(
        "accounts.Profile", on_delete=models.PROTECT, related_name='messages')
    room = models.ForeignKey(
        "Room", on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    send_date = jmodels.jDateTimeField(auto_now_add=True)

    def display_message_date(self):
        """ display message send date for show room for exampla : 1 d ago , 25 m age """

        display_send_date = timezone.now() - self.send_date

        days = display_send_date.days

        seconds = display_send_date.seconds

        hours = seconds // 3600

        minutes = (seconds % 3600) // 60

        if display_send_date < timedelta(minutes=1):
            display_send_date = f"{seconds} s ago"

        elif display_send_date < timedelta(minutes=60):
            display_send_date = f"{minutes} m ago"

        elif display_send_date > timedelta(minutes=60):
            display_send_date = f"{hours} h ago"

        else:
            display_send_date = f"{days} d ago"

        return display_send_date

    def __str__(self):
        return f"{self.author.username}: {self.text[:10]}"

    class Meta:
        ordering = ["-send_date"]


class Contact(models.Model):
    owner = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="contacts")
    contact_user = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="owners")
    created_date = jmodels.jDateTimeField(auto_now_add=True)
    updated_date = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f"owner: {self.owner.username} - {self.contact_user.username}"

    class Meta:
        ordering = ["-created_date", '-updated_date']
        unique_together = ['owner', 'contact_user']
