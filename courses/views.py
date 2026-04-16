from django.shortcuts import render, redirect
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def add_course(request):
    if request.method == "POST":
        Course.objects.create(
            name=request.POST['name'],
            code=request.POST['code'],
            instructor=request.POST['instructor']
        )
        return redirect('course_list')

    return render(request, 'courses/add_course.html')