from re import template
import datetime
from django.forms import ValidationError
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages



from .models import Student, Study, Course
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
        try:
            student = Student.objects.get(student_user=self.request.user)
        except Student.DoesNotExist:
            return None
        return student.courses.all()


class CourseAddView(generic.ListView):
    template_name = 'study/courseAdd.html'
    context_object_name = 'course_add_form'

    def get_queryset(self):
        query = self.request.GET.get('q')
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')

        if query:
            if query1:
                if query2:
                    return Course.objects.filter(subject__icontains=query).filter(number__icontains=query1).filter(name__icontains=query2).order_by("number")
                else:
                    return Course.objects.filter(subject__icontains=query).filter(number__icontains=query1).order_by("number")
            elif query2:
                return Course.objects.filter(subject__icontains=query).filter(name__icontains=query2).order_by("number")
            else:
                return Course.objects.filter(subject__icontains=query).order_by("number")
        if query1:
            if query2:
                return Course.objects.filter(number__icontains=query1).filter(name__icontains=query2).order_by("number")
            else:
                return Course.objects.filter(number__icontains=query1).order_by("number")
        if query2:
            return Course.objects.filter(name__icontains=query2).order_by("number")
        else:
            return Course.objects.order_by("subject")

def uploadCourse(request):

    course = Course.objects.get(subject=request.POST['subject'], number=request.POST['number'])
    course.roster.add(Student.objects.get(student_user=request.user))

    return HttpResponseRedirect(reverse('study:courses'))

    # if (len(request.POST['subject']) == 0 or len(request.POST['course_number']) == 0 or len(request.POST['course_name']) == 0 or len(request.POST['course_section']) == 0):
    #     return render(request, 'study/courseAdd.html', {
    #         'error_message': "One or more required fields were left empty.",
    #     })
    # elif Course.objects.filter(subject=request.POST['subject'], course_number=request.POST['course_number'], course_name=request.POST['course_name'], course_section=request.POST['course_section'], student_course=request.user):
    #     return render(request, 'study/courseAdd.html', {
    #         'error_message': "This course has already been added.",
    #     })
    # else:
    #     Course.objects.create(subject=request.POST['subject'], course_number=request.POST['course_number'],
    #                           course_name=request.POST['course_name'], course_section=request.POST['course_section'], student_course=request.user)

    # return HttpResponseRedirect(reverse('study:courses'))


def MyAccountView(request):

    stud, _ = Student.objects.get_or_create(student_user=request.user)

    return render(request, 'study/myAccount.html', {
        'first_name': stud.first_name,
        'last_name': stud.last_name,
        'computing_id': stud.computing_id,
        'pref_name': stud.pref_name,
        'school_year': stud.school_year,
        'bio': stud.bio,
    })


def uploadProfile(request):

    stud = Student.objects.get(student_user=request.user)

    if request.method == "POST":
        stud.first_name = request.POST['first_name']
        stud.last_name = request.POST['last_name']
        stud.computing_id = request.POST['computing_id']
        stud.pref_name = request.POST['pref_name']
        stud.school_year = request.POST['school_year']
        stud.bio = request.POST['bio']
        stud.save()

    return HttpResponseRedirect(reverse('study:my-account'))


class SessionView(generic.ListView):
    template_name = 'study/sessions.html'
    context_object_name = 'sessions_list'
    
    def get_queryset(self):
        student = Student.objects.get(student_user=self.request.user)
        sessions = Study.objects.filter(organizer=student)
        return sessions  

class SessionAddView(generic.ListView):
    template_name = 'study/addStudy.html'
    context_object_name = 'session_add_form'

    def get_queryset(self):
        try:
            student = Student.objects.get(student_user=self.request.user)
        except Student.DoesNotExist:
            return None
        return student.courses.all()

def uploadSession(request):
    if (
        ValidationError
        #if no course picked
        ):
        messages.error(request, 'Date was inputted wrong. Please use the format in the box.')
        return HttpResponseRedirect(reverse('study:add-session'))
        #fails to show classes again if this message pops up
        
    else:

        stud = Student.objects.get(student_user=request.user)

        Study.objects.create(

            organizer = stud,
            date = request.POST['date'],
            location = request.POST['location'],
            course = Course.objects.get(id = request.POST['courseSession']), #update after we get courses working


        )

        #does not account for attendees

        return HttpResponseRedirect(reverse('study:sessions'))

class SessionRemoveView(generic.ListView):
    template_name = 'study/removeStudy.html'
    context_object_name = 'remove_sessions_list'
    
    def get_queryset(self):
        student = Student.objects.get(student_user=self.request.user)
        sessions = Study.objects.filter(organizer=student)
        return sessions 

def deleteSession(request):
    Study.objects.get(id = request.POST['removeSession']).delete()

    return HttpResponseRedirect(reverse('study:sessions'))
