from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_google_maps import fields as map_fields

# Create your models here.

class Location(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Study(models.Model):
    organizer = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField()
    attendees = models.ManyToManyField(Student, related_name='student_attendees')
    location = models.CharField(max_length=30)


class Section(models.Model):
    name = models.CharField(max_length=30)
    class_number = models.CharField(max_length=30)
    sessions = models.ManyToManyField(Study, related_name='study_sessions')


class Course(models.Model):
    subject = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    sections = models.ManyToManyField(Section, related_name='course_section')