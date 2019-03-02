import datetime
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)

    def is_busy_today(self):
        today = datetime.date.today()
        reservation_today = self.reservation_set.filter(date=today)
        if len(reservation_today) > 0:
            return True
        else:
            return False


class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()

