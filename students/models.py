from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Course



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    course = models.CharField(max_length=100, null=True, blank=True)
    
    
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    image = models.ImageField(upload_to='students/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', default='default.png')

    def __str__(self):
        return self.user.username
    
    
class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    STATUS = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return f"{self.student} - {self.status}"
