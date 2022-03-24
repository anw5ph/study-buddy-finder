<<<<<<< HEAD
# Create your models here.

import datetime

from django import forms
from django.db import models
from django.contrib import admin

import gdata.service
import gdata.calendar.service

from managers import CalendarManager, EventManager

_services = {}

class Account(models.Model):
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	def __unicode__(self):
	    return u'%s' % self.email
	
	def _get_service(self):
		if not _services.has_key(self.email):
			_service = gdata.calendar.service.CalendarService()
			#_service.source = 'ITSLtd-Django_Google-%s' % VERSION
			_service.email = self.email
			_service.password = self.password
			_service.ProgrammaticLogin()
			_services[self.email] = _service
		return _services[self.email]
	service = property(_get_service, None)
	
	def get_own_calendars(self):
		cals = self.service.GetOwnCalendarsFeed()
		result = []
		for i, cal in enumerate(cals.entry):
			result.append(Calendar.objects.get_or_create(self, cal))
		return result

class Calendar(models.Model):
	objects = CalendarManager()
	account = models.ForeignKey(Account)
	uri = models.CharField(max_length = 255, unique = True)
	title = models.CharField(max_length = 100)
	where = models.CharField(max_length = 100, blank = True)
	timezone = models.CharField(max_length = 100, blank = True)
	summary = models.TextField()
	feed_uri = models.CharField(max_length = 255, blank = True)
	def __unicode__(self):
		return self.title
	def get_events(self):
		events = self.account.service.GetCalendarEventFeed(uri = self.feed_uri)
		result = []
		for i, event in enumerate(events.entry):
			result.append(Event.objects.get_or_create(self, event))
		return result

class Event(models.Model):
	objects = EventManager()
	uri = models.CharField(max_length = 255, unique = True)
	calendar = models.ForeignKey(Calendar)
	title = models.CharField(max_length = 255)
	edit_uri = models.CharField(max_length = 255)
	view_uri = models.CharField(max_length = 255)
	content = models.TextField(blank = True)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	where = models.CharField(max_length = 255)
	def __unicode__(self):
		return u'%s' % (self.title)
=======
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
>>>>>>> cecdc89f6cd020952c12fd16931b6a96bca57845
