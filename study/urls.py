# from django.urls import path
# from . import views

# app_name = 'study'
# urlpatterns = [
#     # Study sessions for a course
#     path('<int:course-number>-<int:course-section>/', views.AllSessionView.as_view(), name='all-sessions'),
#     # Individual study session
#     path('<int:course-number>-<int:course-section>/session/<int:pk>/', views.SessionView.as_view(), name='session'),
#     # Add study session
#     path('<int:course-number>-<int:course-section>/session-add/', views.AddSession.as_view(), name='add-session'),
#     # Add course
#     path('course-add/', views.AddCourse.as_view(), name='add-course'),
# ]