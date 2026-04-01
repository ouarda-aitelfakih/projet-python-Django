from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def is_single_day(self):
        return self.end_date is None or self.end_date == self.start_date

    def duration(self):
        if self.is_single_day():
            return 1
        return (self.end_date - self.start_date).days + 1