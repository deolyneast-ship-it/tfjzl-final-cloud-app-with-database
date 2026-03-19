from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # ... your existing paths (index, course_details, etc.)
    
    # TASK 6: Submit path
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # TASK 6: Show Exam Result path (Must include submission_id)
    path('course/<int:course_id>/submission/<int:submission_id>/result/', 
         views.show_exam_result, name='show_exam_result'),
]
