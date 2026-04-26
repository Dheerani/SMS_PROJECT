from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('teacher/edit/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('teacher/<int:id>/', views.teacher_profile, name='teacher_profile'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('attendance/teacher/report/', views.teacher_attendance_report, name='teacher_attendance_report'),
    path('attendance/teacher/monthly/', views.monthly_teacher_report, name='monthly_teacher_report'),
    path('teacher/result/<int:teacher_id>/', views.teacher_result, name='teacher_result'),
    path('teacher/profile/<int:id>/', views.teacher_profile, name='teacher_profile')]   