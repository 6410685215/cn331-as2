from django.shortcuts import render
from users.models import Student
from .models import Course, Enroll
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'course/course.html')

def page_course(request):
    user = request.user
    admin = user.is_staff
    course = Course.objects.all()
    enroll = Enroll.objects.filter(student_id=user)
    enroll = enroll.values_list('course_id', flat=True)    

    return render(request, 'course/page_course.html', { 'username': user,
                                                        'admin': admin,
                                                        'courses': course,
                                                        'enroll': enroll,})

def page_user(request):
    user = request.user
    admin = user.is_staff
    if admin:
        return render(request, 'course/page_user.html', { 'username': user,
                                                          'admin': admin,})
    user_s = Student.objects.get(ID=user)
    return render(request, 'course/page_user.html', { 'username': user,
                                                      'admin': admin,
                                                      'name': user_s.get_full_name(), 
                                                      'email': user_s.email,})

def page_board(request):
    user = request.user
    admin = user.is_staff
    my_course = Enroll.objects.filter(student_id=user)
    enroll = Course.objects.filter(ID__in=my_course.values_list('course_id', flat=True))
    
    return render(request, 'course/page_board.html', { 'username': user,
                                                       'admin': admin,
                                                       'courses': enroll,})
    
def course_enroll(request):
    user = request.user
    admin = user.is_staff
    if admin:
        return page_course(request)
    
    course = Course.objects.get(ID=request.POST['course_id'])
    course.quota -= 1
    course.enrolled += 1
    if course.quota < 0:
        return page_course(request)
    course.save()
    course_enroll = Enroll(student_id=user, course_id=course)
    course_enroll.save()
    return page_course(request)
    
def course_drop(request):
    user = request.user
    admin = user.is_staff
    course = Course.objects.get(ID=request.POST['course_id'])
    course.quota += 1
    course.enrolled -= 1
    course.save()
    if admin:
        user_i = User.objects.get(username=request.POST['user_id'])
        course_enroll = Enroll.objects.get(student_id=user_i, course_id=course)
        print(course_enroll)
        course_enroll.delete()
        return manager(request)
    
    course_enroll = Enroll.objects.get(student_id=user, course_id=course)
    course_enroll.delete()
    return page_board(request)

def manager(request):
    user = request.user
    admin = user.is_staff
    dropdown = Course.objects.all()
    print(request.method)
    if dropdown.count() == 0:
        return render(request, 'course/manager.html', { 'username': user,
                                                        'admin': admin,
                                                        'courses': None, 
                                                        'enroll': None,
                                                        'dropdown': dropdown,})
    if request.method == "GET":
        post = Course.objects.all()[:1].get()
        enroll = Enroll.objects.filter(course_id=post.ID)
        enroll = Student.objects.filter(ID__in=enroll.values_list('student_id', flat=True))
        return render(request, 'course/manager.html', { 'username': user,
                                                        'admin': admin,
                                                        'courses': post, 
                                                        'enroll': enroll,
                                                        'dropdown': dropdown,})
    
    post = Course.objects.get(ID=request.POST['course_id'])
    enroll = Enroll.objects.filter(course_id=post.ID)
    enroll = Student.objects.filter(ID__in=enroll.values_list('student_id', flat=True))
    return render(request, 'course/manager.html', { 'username': user,
                                                    'admin': admin,
                                                    'courses': post, 
                                                    'enroll': enroll,
                                                    'dropdown': dropdown,})