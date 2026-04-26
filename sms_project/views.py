from django.shortcuts import render
from .import Student, Teacher

def global_search(request):
    query = request.GET.get('q')

    students = []
    teachers = []

    if query:
        students = Student.objects.filter(name__icontains=query)
        teachers = Teacher.objects.filter(name__icontains=query)

    return render(request, 'search_results.html', {
        'query': query,
        'students': students,
        'teachers': teachers
    })