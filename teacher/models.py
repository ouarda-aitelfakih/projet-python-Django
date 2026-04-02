from django.db import models

class Teacher(models.Model):
    GENDER_CHOICES = [('Male','Male'), ('Female','Female')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    joining_date = models.DateField()
    qualification = models.CharField(max_length=100)
    teacher_image = models.ImageField(upload_to='teachers/', blank=True)
    department = models.ForeignKey(
        'department.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    # ← Référence string pour éviter l'import circulaire
    user = models.OneToOneField(
        'home_auth.CustomUser',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='teacher_profile'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']