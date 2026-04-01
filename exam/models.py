from django.db import models
from subjects.models import Subject
from student.models import Student

# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)
    total_marks = models.IntegerField(default=100)

    def __str__(self):
        return f'{self.name} - {self.subject.name}'
    
class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    marks_obtained = models.FloatField(default=0)
    grade = models.CharField(max_length=5, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        # Un étudiant ne peut avoir qu'un seul résultat par examen
        unique_together = ['exam', 'student']
    
    def __str__(self):
        return f'{self.student} — {self.exam} : {self.marks_obtained}'