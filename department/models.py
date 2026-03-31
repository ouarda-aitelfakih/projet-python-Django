from django.db import models

# Create your models here.

class Department(models.Model):
    # Nom du département — obligatoire et unique
    name = models.CharField(max_length=100, unique=True)
    # Chef du département — facultatif (blank=True)
    head_of_department = models.CharField(max_length=100, blank=True)
    # Description — facultatif
    description = models.TextField(blank=True)
    # Date de création — remplie automatiquement
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        # Ce qui s'affiche dans l'admin et les selects
        return self.name
    
    class Meta:
        ordering = ['name'] # Trier par nom alphabétiquement

