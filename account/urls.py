from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/instructor/', views.InstructorSignupView.as_view()),
    path('signup/student/', views.StudentSignupView.as_view()),
    
    path('profile/instructor/', views.instructor_profile, name='instructor-profile'),
    path('profile/student/', views.student_profile, name='student-profile'),
    
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    path('dashboard/instructor/', views.InstructorOnlyView.as_view(), name='instructor_dashboard'),
    path('dashboard/student/', views.StudentOnlyView.as_view(), name='student_dashboard'),
    
]
