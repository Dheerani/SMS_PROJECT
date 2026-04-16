from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from .forms import TeacherForm
from django.contrib.auth.decorators import login_required

from .models import TeacherAttendance

@login_required
def monthly_teacher_report(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    attendance = TeacherAttendance.objects.all()

    if month and year:
        attendance = attendance.filter(
            date__month=month,
            date__year=year
        )

    return render(request, 'teachers/monthly_teacher_report.html', {
        'attendance': attendance
    })
    

@login_required
def teacher_attendance_report(request):
    teacher_id = request.GET.get('teacher')

    if teacher_id:
        attendance = TeacherAttendance.objects.filter(teacher_id=teacher_id)
    else:
        attendance = TeacherAttendance.objects.all()

    teachers = Teacher.objects.all()

    return render(request, 'teachers/teacher_attendance_report.html', {
        'attendance': attendance,
        'teachers': teachers
    })

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})


@login_required
def add_teacher(request):
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    return render(request, 'teachers/add_teacher.html', {'form': form})


@login_required
def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher.delete()
    return redirect('teacher_list')

@login_required
def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    form = TeacherForm(instance=teacher)

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')

    return render(request, 'teachers/edit_teacher.html', {'form': form})    



def teacher_profile(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    return render(request, 'teachers/teacher_profile.html', {'teacher': teacher})



@login_required
def teacher_dashboard(request):
    teachers = Teacher.objects.all()

    total_teachers = teachers.count()

    context = {
        'teachers': teachers,
        'total_teachers': total_teachers,
    }
    return render(request, 'teachers/teacher_dashboard.html', context)


from .models import Teacher, TeacherAttendance

def teacher_attendance(request):
    teachers = Teacher.objects.all()

    if request.method == "POST":
        print("POST HIT", request.POST)

        teacher_id = request.POST.get("teacher_id")
        status = request.POST.get("status")

        if teacher_id and status:
            teacher = Teacher.objects.get(id=teacher_id)

            TeacherAttendance.objects.create(
                teacher=teacher,
                status=status
            )

        return redirect('teacher_attendance')

    return render(request, "teachers/teacher_attendance.html", {
        "teachers": teachers
    })