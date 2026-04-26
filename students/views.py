from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, StudentAttendance, Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from courses.models import Course
from django.db import transaction
from datetime import datetime
from .models import Student, StudentAttendance
from teachers.models import Teacher

@login_required
def global_search(request):
    query = request.GET.get('q')

    students = []
    teachers = []

    if query:
        students = Student.objects.filter(name__icontains=query)
        teachers = Teacher.objects.filter(name__icontains=query)

    return render(request, 'students/search_results.html', {
        'query': query,
        'students': students,
        'teachers': teachers
    })

@login_required
def student_result(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    attendance = StudentAttendance.objects.filter(student=student)

    total = attendance.count()
    present = attendance.filter(status='Present').count()
    absent = attendance.filter(status='Absent').count()

    percentage = (present / total * 100) if total > 0 else 0

    context = {
        'student': student,
        'total': total,
        'present': present,
        'absent': absent,
        'percentage': round(percentage, 2),
    }

    return render(request, 'students/student_result.html', context)



#monthly report
@login_required
def monthly_student_report(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    attendance = StudentAttendance.objects.all()

    if month and year:
        attendance = attendance.filter(
            date__month=month,
            date__year=year
        )

    return render(request, 'students/monthly_report.html', {
        'attendance': attendance
    })


@login_required
def attendance_report(request):
    student_id = request.GET.get('student')

    if student_id:
        attendance = StudentAttendance.objects.filter(student_id=student_id)
    else:
        attendance = StudentAttendance.objects.all()

    students = Student.objects.all()

    return render(request, 'students/attendance_report.html', {
        'attendance': attendance,
        'students': students
    })
    
    

@login_required
def student_attendance(request):
    students = Student.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        status = request.POST.get("status")

        if student_id and status:
            with transaction.atomic():   # ✅ FIX
                student = Student.objects.get(id=student_id)

                StudentAttendance.objects.create(
                    student=student,
                    status=status
                )

        return redirect('student_attendance')

    return render(request, "students/student_attendance.html", {
        "students": students
    })

# PROFILE
@login_required
def profile(request):
    return render(request, 'students/profile.html')


@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user = request.user

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        if request.FILES.get('image'):
            profile.image = request.FILES['image']
            profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    return render(request, 'students/update_profile.html', {
        'profile': profile
    })



# DASHBOARD
@login_required
def student_dashboard(request):
    students = Student.objects.all().order_by('-id')[:5]
    total_students = Student.objects.count()

    return render(request, 'students/student_dashboard.html', {
        'students': students,
        'total_students': total_students,
    })


# AUTH
def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'students/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'students/register.html')



def home(request):
    return render(request, 'students/home.html')



@login_required
def student_list(request):
    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'students/student_list.html', {
        'students': students,
        'query': query
    })



@login_required
def add_student(request):
    courses = Course.objects.all()

    if request.method == "POST":
        name = request.POST['name']
        roll_no = request.POST.get('roll_no')
        email = request.POST['email']
        course_id = request.POST.get('course')
        image = request.FILES.get('image')

        course = None
        if course_id and course_id.isdigit():
            course = Course.objects.get(id=int(course_id))

        Student.objects.create(
            name=name,
            roll_no=roll_no,
            email=email,
            course=course,
            image=image
        )

        return redirect('student_list')

    return render(request, 'students/add.html', {
        'courses': courses
    })


# =========================
# DELETE STUDENT (FIXED REDIRECT)
# =========================
@login_required
def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('student_list')   # ✅ FIXED


# =========================
# UPDATE STUDENT
# =========================
from courses.models import Course

@login_required
def update_student(request, id):
    student = Student.objects.get(id=id)
    courses = Course.objects.all()

    if request.method == "POST":
        student.name = request.POST['name']
        student.roll_no = request.POST['roll_no']
        student.email = request.POST['email']

        course_id = request.POST.get('course')

        if course_id and course_id.isdigit():
            student.course = Course.objects.get(id=int(course_id))

        if request.FILES.get('image'):
            student.image = request.FILES.get('image')

        student.save()
        return redirect('student_list')

    return render(request, 'students/update.html', {
        'student': student,
        'courses': courses
    })