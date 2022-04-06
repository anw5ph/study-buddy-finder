from django.contrib import admin
from .models import Student, Study, Course  # , Location
# from django_google_maps import widgets as map_widgets
# from django_google_maps import fields as map_fields

# class LocationAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
#     }

# admin.site.register(Location, LocationAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('computing_id', 'last_name', 'first_name',
                    'pref_name', 'school_year', 'bio', 'student_user')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'number', 'name')


admin.site.register(Student, StudentAdmin)
admin.site.register(Study)
admin.site.register(Course, CourseAdmin)
