from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE

class UserAvailability(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.day_of_week}"

class Booking(models.Model):
    guest_name = models.CharField(max_length=100)
    availability = models.ForeignKey(UserAvailability, on_delete=CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.guest_name} - {self.date} ({self.start_time} to {self.end_time})"
