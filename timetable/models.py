from django.db import models

# Create your models here.
from django.db import models
from subjects.models import Subject
from teacher.models import Teacher

class TimeTable(models.Model):
    DAY_CHOICES = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
    ]

    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.day} - {self.subject.name} ({self.start_time})"

    class Meta:
        ordering = ['day', 'start_time']
