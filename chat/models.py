from django.db import models
from django_jalali.db import models as jmodels

# Create your models here.


class Room(models.Model):
    users = models.ManyToManyField("accounts.Profile")
    created_date = jmodels.jDateTimeField(auto_now_add=True)
    updated_date = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f"room: {self.pk}"

    class Meta:
        ordering = ["-created_date", '-updated_date']


class Message(models.Model):
    author = models.ForeignKey("accounts.Profile", on_delete=models.PROTECT)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    text = models.TextField()
    send_date = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.text[:10]}"

    class Meta:
        ordering = ["-send_date"]


class Contact(models.Model):
    owner = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="contacts")
    username = models.CharField(max_length=200)
    created_date = jmodels.jDateTimeField(auto_now_add=True)
    updated_date = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f"owner: {self.owner.username} - {self.username}"

    class Meta:
        ordering = ["-created_date", '-updated_date']
