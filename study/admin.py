from django.contrib import admin

# Register your models here.
from .models import Student, Study, Section, Course

admin.site.register(Student)
admin.site.register(Study)
admin.site.register(Section)
admin.site.register(Course)