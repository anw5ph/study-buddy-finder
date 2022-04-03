from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_google_maps import fields as map_fields
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Location(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    def __str__(self):
        return self.address


class Student(models.Model):
    student_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=None)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    computing_id = models.CharField(max_length=7, default='')
    pref_name = models.CharField(max_length=30, default='')
    school_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)], default=1)
    bio = models.CharField(max_length=2600, default='')

    def __str__(self):
        return str(self.student_user.pk)


class Study(models.Model):
    organizer = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField()
    attendees = models.ManyToManyField(
        Student, related_name='student_attendees')
    location = models.CharField(max_length=30)
    study_subject = models.CharField(max_length=4, default='')
    study_number = models.CharField(max_length=4, default='')
    study_name = models.CharField(max_length=100, default='')
    study_section = models.CharField(max_length=3, default='')

    def __str__(self):
        return self.study_subject + " " + self.study_number + " " + self.study_name


class Course(models.Model):
    subject = models.CharField(max_length=4)
    course_number = models.CharField(max_length=4, default='')
    course_name = models.CharField(max_length=100, default='')
    course_section = models.CharField(max_length=3, default='')
    student_course = models.ForeignKey(
        User, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.subject + " " + self.course_number
