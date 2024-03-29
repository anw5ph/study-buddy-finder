from django.contrib import admin
from .models import Student, Study, Course
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class StudentAdmin(admin.ModelAdmin):
    list_display = ('computing_id', 'last_name', 'first_name',
                    'pref_name', 'school_year', 'bio', 'student_user')
    search_fields = ['last_name']
    ordering = ['id']


class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'number', 'name')
    list_filter = ['subject']
    search_fields = ['name']
    ordering = ['subject']
    readonly_fields = ('subject', 'number', 'name', 'roster')


class StudyAdmin(admin.ModelAdmin):
    list_display = ('date', 'address', 'course', 'organizer')
    list_filter = ['date']
    search_fields = ['course']
    ordering = ['date']
    readonly_fields = ('organizer', 'attendees')
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }


admin.site.register(Student, StudentAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Course, CourseAdmin)
