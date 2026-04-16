from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('add/', views.add_student, name='add_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('update/<int:id>/', views.update_student, name='update_student'),
    path('students/', views.student_list, name='student_list'),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('attendance/', views.student_attendance, name='student_attendance'),
    path('attendance/student/', views.student_attendance, name='student_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    path('attendance/student/monthly/', views.monthly_student_report, name='monthly_student_report'),
]

