from django.db import models
from students.models import Student
from teachers.models import Teacher

class Attendance(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    status = models.CharField(max_length=10)  # Present / Absent
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student.name