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
    path('course-add/upload', views.uploadCourse, name='upload'),

     # Remove a course
    path('course-add/remove', views.CourseRemoveView.as_view(), name='remove-course'),

    # See sessions for a course
    path('<int:course_pk>/sessions/',
         views.CourseSessionView, name='course-session'),

    # View sessions
    path('sessions/', views.SessionView.as_view(), name='sessions'),

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
