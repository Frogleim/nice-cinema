from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    columns = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    room = models.ForeignKey(Room, related_name='movies', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"


class Seat(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    row = models.IntegerField()
    number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    movie = models.ForeignKey(Movie, related_name='seats', on_delete=models.CASCADE)

    def __str__(self):
        return f"Row {self.row} - Seat {self.number} ({self.status})"
