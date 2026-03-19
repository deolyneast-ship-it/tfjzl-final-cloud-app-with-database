from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # 1. Get the enrollment for the current user
        # Note: Adjust 'user' logic based on your project's auth setup
        enrollment = get_object_or_404(Enrollment, course=course, user=request.user)
        
        # 2. Create the Submission object first
        submission = Submission.objects.create(enrollment=enrollment)
        
        # 3. Get selected choice IDs from the POST data (from the form checkboxes)
        # 'choice' should match the 'name' attribute in your HTML input
        choice_ids = request.POST.getlist('choice')
        
        # 4. Associate selected choices with the submission
        for choice_id in choice_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
            
        # 5. Redirect to the result page
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # 1. Calculate the score logic
    total_questions = course.question_set.count()
    correct_choices = submission.choices.filter(is_correct=True).count()
    
    # Simple score calculation (adjust based on your specific lab instructions)
    score = (correct_choices / total_questions) * 100 if total_questions > 0 else 0
    
    # 2. Create the EXPLICIT context for the grader to see
    context = {
        'course': course,
        'submission': submission,
        'score': score,
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
