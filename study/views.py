# from django.utils import timezone
# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.views import generic

# from .models import Student, Study, Section, Course
# from .forms import LocationForm

# Create your views here.

# class landingPageView(generic.ListView):
#     model = Location
#     template_name = 'study/landing.html'

#     def get_queryset(self):
#         return Location.objects.all()

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

