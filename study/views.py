from re import template
from datetime import datetime
from django.db.models.functions import Now
from django.forms import ValidationError
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from requests import session


from .models import Student, Study, Course


class CourseView(generic.ListView):
    template_name = 'study/courses.html'
    context_object_name = 'courses_list'

    def get_queryset(self):
        student, _ = Student.objects.get_or_create(
            student_user=self.request.user)
        return student.courses.all()


def CourseSessionView(request, course_pk):

    course_wanted = get_object_or_404(Course, pk=course_pk)
    try:
        # sessions_wanted = (Study.objects.filter(
        #     course=course_wanted)).values('date', 'address', 'pk', 'organizer', 'attendees', 'course')
        # now = datetime.today()
        sessions_wanted = Study.objects.filter(
            course=course_wanted, date__gte=Now())
    except:
        return messages.error(request, 'There are no upcoming study sessions at this time for the requested course.')

    print(str(sessions_wanted))

    return render(request, 'study/courseSessions.html', {'session_list': sessions_wanted})


def SessionMoreView(request, session_pk):

    session_wanted = get_object_or_404(Study, pk=session_pk)
    stud = Student.objects.get(student_user=request.user)
    buttonswitch = ''
    for person in session_wanted.attendees.all():
        if stud == person:
            buttonswitch = stud

    return render(request, 'study/sessionInfo.html', {
        'organizer': session_wanted.organizer,
        'date': session_wanted.date,
        'attendees': session_wanted.attendees,
        'address': session_wanted.address,
        'course': session_wanted.course,
        'pk': session_wanted.pk,
        'latitude': session_wanted.latitude,
        'longitude': session_wanted.longitude,
        # added this for html file
        'student': stud,
        'det': buttonswitch
    })


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

    student = Student.objects.get(student_user=request.user)
    course = Course.objects.get(
        subject=request.POST['subject'], number=request.POST['number'])
    if course not in student.courses.all():
        course.roster.add(student)
    else:
        messages.error(request, 'Already added this course.')
    return HttpResponseRedirect(reverse('study:courses'))


class CourseRemoveView(generic.ListView):
    template_name = 'study/removeCourse.html'
    context_object_name = 'course_remove_list'

    def get_queryset(self):
        try:
            student = Student.objects.get(student_user=self.request.user)
        except Student.DoesNotExist:
            return None
        return student.courses.all()


def deleteCourse(request):

    try:

        student = Student.objects.get(student_user=request.user)
        course = Course.objects.get(id=request.POST['removeCourse'])

        studies = Study.objects.all()

        for study in studies:
            if(study.organizer == student and study.course == course):
                study.delete()

        course.roster.remove(student)

        return HttpResponseRedirect(reverse('study:courses'))

    except:

        messages.error(
            request, 'Please pick a class to remove or click My Courses to go back.')
        return HttpResponseRedirect(reverse('study:remove-course'))


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


def attendSession(request):

    session = get_object_or_404(Study, pk=request.POST['session_id'])
    stud = get_object_or_404(Student, student_user=request.user)

    if request.method == "POST":
        if stud not in session.attendees.all():
            session.attendees.add(stud)
            session.save()

    return HttpResponseRedirect(reverse('study:sessions'))


def leaveSession(request):

    session = get_object_or_404(Study, pk=request.POST['session_id'])
    stud = get_object_or_404(Student, student_user=request.user)

    if stud == session.organizer:
        session.delete()

        return HttpResponseRedirect(reverse('study:sessions'))



    if request.method == "POST":
        if stud in session.attendees.all():
            session.attendees.remove(stud)
            session.save()
            if len(session.attendees.all()) == 0:
                session.delete()
        else:
            messages.error(
                request, "You are not part of any sessions, join a session to leave one first!")
            HttpResponseRedirect(reverse('study:sessions'))

    return HttpResponseRedirect(reverse('study:sessions'))


class SessionView(generic.ListView):
    template_name = 'study/sessions.html'
    context_object_name = 'sessions_list'

    def get_queryset(self):
        student, _ = Student.objects.get_or_create(
            student_user=self.request.user)
        sessions = Study.objects.filter(attendees=student)
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

    try:

        stud = Student.objects.get(student_user=request.user)

        session = Study.objects.create(

            organizer=stud,
            date=request.POST['date'],
            address=request.POST['address'],
            latitude=request.POST['latitude'],
            longitude=request.POST['longitude'],
            course=Course.objects.get(id=request.POST['courseSession']),


        )

        # Add student to list off attendes for said study object, Organizer is part of attendees but not all attendees are organizers for the study object
        session.attendees.add(stud)

        return HttpResponseRedirect(reverse('study:sessions'))

    except(ValidationError):
        messages.error(
            request, 'Date was inputted wrong. Please use the format in the box.')
        return HttpResponseRedirect(reverse('study:add-session'))


class SessionRemoveView(generic.ListView):
    template_name = 'study/removeStudy.html'
    context_object_name = 'remove_sessions_list'

    def get_queryset(self):
        student = Student.objects.get(student_user=self.request.user)
        sessions = Study.objects.filter(organizer=student)
        return sessions


def deleteSession(request):

    try:

        Study.objects.get(id=request.POST['removeSession']).delete()
        return HttpResponseRedirect(reverse('study:sessions'))

    except:

        messages.error(
            request, 'Please pick a session to remove or click My Sessions to go back.')
        return HttpResponseRedirect(reverse('study:remove-session'))
