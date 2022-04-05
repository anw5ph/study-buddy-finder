from django.urls import path
from . import views

app_name = 'study'
urlpatterns = [
    


    # View courses
    path('courses/', views.CourseView.as_view(), name='courses'),
    # Add course
    path('course-add/', views.CourseAddView.as_view(), name='course-add'),

    # Upload course
    path('course-add/uploadCourse', views.uploadCourse, name='uploadCourse'),

    # View sessions
    path('sessions/', views.SessionView.as_view(), name='sessions'),
    # Add session
    path('session-add/', views.SessionAddView.as_view(), name='session-add'),

    # Upload session
    path('session-add/uploadSession', views.uploadSession, name='uploadSession'),

    # Study sessions for a course
    #path('<int:course-number>-<int:course-section>/', views.AllSessionView.as_view(), name='all-sessions'),
    # Individual study session
    #path(/session/<int:pk>/', views.SessionView.as_view(), name='session'),
    # Add study session

    # My Account
    path('my-account', views.MyAccountView, name='my-account'),

    path('my-account/update-profile/upload',
         views.uploadProfile, name='upload-profile'),

]
