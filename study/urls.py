from django.urls import path
from . import views

app_name = 'study'
urlpatterns = [
    # Study sessions for a course
    #path('<int:course-number>-<int:course-section>/', views.AllSessionView.as_view(), name='all-sessions'),
    # Individual study session
    #path('<int:course-number>-<int:course-section>/session/<int:pk>/', views.SessionView.as_view(), name='session'),
    # Add study session
    #path('<int:course-number>-<int:course-section>/session-add/', views.StudyAddView.as_view(), name='add-session'),
    # Upload study session
    #path('<int:course-number>-<int:course-section>/session-add/upload', views.addStudy, name='add-session'),

    # View courses
    path('courses/', views.CourseView.as_view(), name='courses'),
    # Add course
    path('course-add/', views.CourseAddView.as_view(), name='course-add'),

    # Upload course
    path('course-add/upload', views.uploadCourse, name='upload'),
    # path('my-account', views.MyAccountView.as_view(), name='my-account'),
]
