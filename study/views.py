from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Location, Student, Study, Course
# from .forms import LocationForm

# Create your views here.

# def map_display(request):
#     location_instance = get_object_or_404()
    
#     if request.method == 'POST':
#         form = LocationForm(request.POST
        
#         if form.is_valid():

# class mapView(generic.DetailView):
#    model = Location
#    template_name = 'study/map.html'

#    def get_queryset(self):
#        return Location.objects     

class CourseView(generic.ListView):
    template_name = 'study/courses.html'
    context_object_name = 'courses_list'

    def get_queryset(self):
        return Course.objects.all()

class CourseAddView(generic.ListView):
    template_name = 'study/courseAdd.html'
    context_object_name = 'course_add_form'

    def get_queryset(self):
        return Course.objects.all()    

def uploadCourse(request):

    if (len(request.POST['subject']) == 0 or len(request.POST['course_number']) == 0 or len(request.POST['course_name']) == 0 or len(request.POST['course_section']) == 0):
        return render(request, 'study/courseAdd.html', {
            'error_message': "One or more required fields were left empty.",
        })

    else:
        Course.objects.create(subject=request.POST['subject'], course_number=request.POST['course_number'], course_name=request.POST['course_name'], course_section=request.POST['course_section'], student_course=request.user)

    return HttpResponseRedirect(reverse('study:course-add'))

class SessionView(generic.ListView):
    template_name = 'study/sessions.html'
    context_object_name = 'sessions_list'

    def get_queryset(self):
        return Study.objects.all()

