from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def course(request):
    return render(request, 'course/index.html', {
        'title': 'Course'
        })