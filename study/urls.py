from django.urls import path
from . import views

app_name = 'study'
urlpatterns = [

    # Study sessions for a course
    #path('<int:course-number>-<int:course-section>/', views.AllSessionView.as_view(), name='all-sessions'),
    # Individual study session
    #path('<int:course-number>-<int:course-section>/session/<int:pk>/', views.SessionView.as_view(), name='session'),



    # View courses
    path('courses/', views.CourseView.as_view(), name='courses'),
    # Add course
    path('course-add/', views.CourseAddView.as_view(), name='course-add'),

    # Upload course
    path('course-add/uploadCourse', views.uploadCourse, name='upload'),

    # See sessions for a course
    path('<int:course_pk>/sessions/',
         views.CourseSessionView, name='course-session'),

    # See more info about a session
    path('<int:session_pk>/info/',
         views.SessionMoreView, name='info'),

    #Attend a session you have not made
    path('session/attend/', views.attendSession, name='add-attendee'),

    #Leave a session you have not made
    path('session/leave/', views.leaveSession, name='remove-attendee'),

    # remove a course
    path('course-remove/', views.CourseRemoveView.as_view(), name='remove-course'),

    path('course-remove/delete', views.deleteCourse, name='removeCourse'),

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

    # Add study session
    path('session-add/', views.SessionAddView.as_view(), name='add-session'),

    # Upload study session
    path('session-add/upload', views.uploadSession, name='uploadSession'),

    # Remove study session
    path('session-remove/', views.SessionRemoveView.as_view(), name='remove-session'),


    path('session-remove/delete', views.deleteSession, name='removeSession'),


    # My Account
    path('my-account', views.MyAccountView, name='my-account'),

    path('my-account/update-profile/upload',
         views.uploadProfile, name='upload-profile'),

    

]
