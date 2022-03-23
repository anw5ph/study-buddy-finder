from django.contrib import admin
from .models import Location, Student, Study, Section, Course
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

admin.site.register(Location, LocationAdmin)
admin.site.register(Student)
admin.site.register(Study)
admin.site.register(Section)
admin.site.register(Course)
