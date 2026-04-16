from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    instructor = models.CharField(max_length=100)

    def __str__(self):
        return self.name
