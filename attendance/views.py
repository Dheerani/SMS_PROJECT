from django.shortcuts import render, redirect
from .models import Attendance
from .forms import AttendanceForm

def mark_attendance(request):

    form = AttendanceForm()

    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_report')

    return render(request, 'attendance/mark_attendance.html', {'form': form})


def attendance_report(request):
    records = Attendance.objects.all()
    return render(request, 'attendance/report.html', {'records': records})
