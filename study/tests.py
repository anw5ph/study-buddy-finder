# Google OAuth tests provided by django-allauth author:
# https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/providers/google/tests.py

from __future__ import absolute_import, unicode_literals

from importlib import import_module
from re import S
from requests.exceptions import HTTPError

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse

from allauth.account import app_settings as account_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, patch
from allauth.tests import TestCase as AuthTestCase

from allauth.socialaccount.providers.google.provider import GoogleProvider

from django.test import TestCase
from .models import Course, Study, Student


@override_settings(
    SOCIALACCOUNT_AUTO_SIGNUP=True,
    ACCOUNT_SIGNUP_FORM_CLASS=None,
    ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.MANDATORY,
)
class GoogleTests(OAuth2TestsMixin, AuthTestCase):
    provider_id = GoogleProvider.id

    def get_mocked_response(
        self,
        family_name="Penners",
        given_name="Raymond",
        name="Raymond Penners",
        email="raymond.penners@example.com",
        verified_email=True,
    ):
        return MockedResponse(
            200,
            """
              {"family_name": "%s", "name": "%s",
               "picture": "https://lh5.googleusercontent.com/photo.jpg",
               "locale": "nl", "gender": "male",
               "email": "%s",
               "link": "https://plus.google.com/108204268033311374519",
               "given_name": "%s", "id": "108204268033311374519",
               "verified_email": %s }
        """
            % (
                family_name,
                name,
                email,
                given_name,
                (repr(verified_email).lower()),
            ),
        )

    def test_google_compelete_login_401(self):
        from allauth.socialaccount.providers.google.views import (
            GoogleOAuth2Adapter,
        )

        class LessMockedResponse(MockedResponse):
            def raise_for_status(self):
                if self.status_code != 200:
                    raise HTTPError(None)

        request = RequestFactory().get(
            reverse(self.provider.id + "_login"), dict(process="login")
        )

        adapter = GoogleOAuth2Adapter(request)
        app = adapter.get_provider().get_app(request)
        token = SocialToken(token="some_token")
        response_with_401 = LessMockedResponse(
            401,
            """
            {"error": {
              "errors": [{
                "domain": "global",
                "reason": "authError",
                "message": "Invalid Credentials",
                "locationType": "header",
                "location": "Authorization" } ],
              "code": 401,
              "message": "Invalid Credentials" }
            }""",
        )
        with patch(
            "allauth.socialaccount.providers.google.views.requests"
        ) as patched_requests:
            patched_requests.get.return_value = response_with_401
            with self.assertRaises(HTTPError):
                adapter.complete_login(request, app, token)

    def test_username_based_on_email(self):
        first_name = "明"
        last_name = "小"
        email = "raymond.penners@example.com"
        self.login(
            self.get_mocked_response(
                name=first_name + " " + last_name,
                email=email,
                given_name=first_name,
                family_name=last_name,
                verified_email=True,
            )
        )
        user = User.objects.get(email=email)
        self.assertEqual(user.username, "raymond.penners")

    def test_email_verified(self):
        test_email = "raymond.penners@example.com"
        self.login(self.get_mocked_response(verified_email=True))
        email_address = EmailAddress.objects.get(
            email=test_email, verified=True)
        self.assertFalse(
            EmailConfirmation.objects.filter(
                email_address__email=test_email).exists()
        )
        account = email_address.user.socialaccount_set.all()[0]
        self.assertEqual(account.extra_data["given_name"], "Raymond")

    def test_user_signed_up_signal(self):
        sent_signals = []

        def on_signed_up(sender, request, user, **kwargs):
            sociallogin = kwargs["sociallogin"]
            self.assertEqual(sociallogin.account.provider, GoogleProvider.id)
            self.assertEqual(sociallogin.account.user, user)
            sent_signals.append(sender)

        user_signed_up.connect(on_signed_up)
        self.login(self.get_mocked_response(verified_email=True))
        self.assertTrue(len(sent_signals) > 0)

    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_HMAC=False)
    def test_email_unverified(self):
        test_email = "raymond.penners@example.com"
        resp = self.login(self.get_mocked_response(verified_email=False))
        email_address = EmailAddress.objects.get(email=test_email)
        self.assertFalse(email_address.verified)
        self.assertTrue(
            EmailConfirmation.objects.filter(
                email_address__email=test_email).exists()
        )
        self.assertTemplateUsed(
            resp, "account/email/email_confirmation_signup_subject.txt"
        )

    def test_email_verified_stashed(self):
        # http://slacy.com/blog/2012/01/how-to-set-session-variables-in-django-unit-tests/
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        request = RequestFactory().get("/")
        request.session = self.client.session
        adapter = get_adapter(request)
        test_email = "raymond.penners@example.com"
        adapter.stash_verified_email(request, test_email)
        request.session.save()

        self.login(self.get_mocked_response(verified_email=False))
        email_address = EmailAddress.objects.get(email=test_email)
        self.assertTrue(email_address.verified)
        self.assertFalse(
            EmailConfirmation.objects.filter(
                email_address__email=test_email).exists()
        )

    def test_account_connect(self):
        email = "user@example.com"
        user = User.objects.create(
            username="user", is_active=True, email=email)
        user.set_password("test")
        user.save()
        EmailAddress.objects.create(
            user=user, email=email, primary=True, verified=True)
        self.client.login(username=user.username, password="test")
        self.login(self.get_mocked_response(
            verified_email=True), process="connect")
        # Check if we connected...
        self.assertTrue(
            SocialAccount.objects.filter(
                user=user, provider=GoogleProvider.id).exists()
        )
        # For now, we do not pick up any new e-mail addresses on connect
        self.assertEqual(EmailAddress.objects.filter(user=user).count(), 1)
        self.assertEqual(EmailAddress.objects.filter(
            user=user, email=email).count(), 1)

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.MANDATORY,
        SOCIALACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.NONE,
    )
    def test_social_email_verification_skipped(self):
        test_email = "raymond.penners@example.com"
        self.login(self.get_mocked_response(verified_email=False))
        email_address = EmailAddress.objects.get(email=test_email)
        self.assertFalse(email_address.verified)
        self.assertFalse(
            EmailConfirmation.objects.filter(
                email_address__email=test_email).exists()
        )

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.OPTIONAL,
        SOCIALACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.OPTIONAL,
    )
    def test_social_email_verification_optional(self):
        self.login(self.get_mocked_response(verified_email=False))
        self.assertEqual(len(mail.outbox), 1)
        self.login(self.get_mocked_response(verified_email=False))
        self.assertEqual(len(mail.outbox), 1)


@override_settings(
    SOCIALACCOUNT_PROVIDERS={
        "google": {
            "APP": {
                "client_id": "app123id",
                "key": "google",
                "secret": "dummy",
            }
        }
    }
)
def create_user():
    email = "user@example.com"
    user = User.objects.create(username="user", is_active=True, email=email)
    user.set_password("test")
    user.save()
    return user


def create_course(subject, number, name):
    return Course.objects.create(subject=subject,number = number, name = name)


# class CourseViewTests(TestCase):

#     def test_no_courses(self):
#         """
#         If no courses have been added, an appropriate message is displayed.
#         """
#         user = create_user()
#         self.client.force_login(user)
#         response = self.client.get(reverse('study:courses'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "You have not added any courses yet!")
#         self.assertQuerysetEqual(response.context['courses_list'], [])

#     def test_one_course(self):
#         """
#         One course is displayed.
#         """
#         user = create_user()
#         self.client.force_login(user)
#         course = create_course("CS", "3240", "Test Course", "1", user)
#         response = self.client.get(reverse('study:courses'))
#         self.assertQuerysetEqual(response.context['courses_list'], [course])

#     def test_multiple_courses(self):
#         """
#         Both courses are displayed.
#         """
#         user = create_user()
#         self.client.force_login(user)
#         course = create_course("CS", "3240", "Test Course", "1", user)
#         course2 = create_course("FREN", "1010", "français", "2", user)
#         response = self.client.get(reverse('study:courses'))
#         self.assertQuerysetEqual(response.context['courses_list'], [course, course2], ordered=False)


# class CourseAddTests(TestCase):
#     """
#     Tests form validation
#     """
#     def test_invalid_course(self):
#         user = create_user()
#         self.client.force_login(user)
#         response = self.client.post(reverse('study:upload'), {'subject':'', 'course_number':'', 'course_name':'', 'course_section':'', 'student_course':user}, follow=True)
#         self.assertContains(response, "One or more required fields were left empty.", html=True)

#     def test_duplicate_course(self):
#         user = create_user()
#         self.client.force_login(user)
#         create_course("CS", "3240", "Test Course", "1", user)
#         response = self.client.post(reverse('study:upload'), {'subject':'CS', 'course_number':'3240', 'course_name':'Test Course', 'course_section':'1', 'student_course':user}, follow=True)
#         self.assertContains(response, "This course has already been added.")

def create_student(student_user, first_name, last_name, computing_id, pref_name, school_year, bio):
    return Student.objects.create(student_user = student_user, first_name = first_name, last_name = last_name, computing_id = computing_id, pref_name = pref_name, school_year = school_year, bio = bio)

def create_study_session(organizer, date, location, course):
    session = Study.objects.create(organizer = organizer, date = date, location = location, course = course)
    session.attendees.add(organizer)
    return session

class SessionAddTests(TestCase):

    def test_invalid_date(self):
        """
        If date is inputted wrong a message is displayed
        """
        user = create_user()
        self.client.force_login(user)
        test_student = create_student(user, 'testfirstname', 'testlastname', 'testcid', 'testpref', int(1), 'test bio')
        test_course = create_course("CS", "3240", "Test Course")
        test_course.roster.add(test_student)


        response = self.client.post(reverse('study:uploadSession'), {'date' : '01/02/2022', 'location' : 'testlocation', 'courseSession' : test_course.id})
        self.assertEqual(response.status_code, 302)
        self.assertRaisesMessage(ValueError, "Date was inputted wrong. Please use the format in the box.")



class SessionViewTests(TestCase):

    def test_no_sessions(self): #works
        """
        If no sessions are available a mesasge is displayed
        """
        user = create_user()
        self.client.force_login(user)
        test_student = create_student(user, 'testfirstname', 'testlastname', 'testcid', 'testpref', int(1), 'test bio')
        test_course = create_course("CS", "3240", "Test Course")
        test_course.roster.add(test_student)
        response = self.client.get(reverse('study:sessions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have not posted or joined any study sessions yet!")
        self.assertQuerysetEqual(response.context['sessions_list'], [])
    
    
    
    def test_one_sessions(self): #works
        """
        One course is displayed.
        """
        user = create_user()
        self.client.force_login(user)
        test_student = create_student(user, 'testfirstname', 'testlastname', 'testcid', 'testpref', int(1), 'test bio')
        test_course = create_course("CS", "3240", "Test Course")
        test_course.roster.add(test_student)
        session1 = create_study_session(test_student, '2022-04-09', 'testloc', test_course)
        response = self.client.get(reverse('study:sessions'))

        #No need for ordered = False if it is just 1 item
        self.assertQuerysetEqual(response.context['sessions_list'], [session1])

    def test_two_sessions(self): #works
        """"
        Two courses are displayed.
        """
        user = create_user()
        self.client.force_login(user)
        test_student = create_student(user, 'testfirstname', 'testlastname', 'testcid', 'testpref', int(1), 'test bio')
        test_course = create_course("CS", "3240", "Test Course")
        test_course.roster.add(test_student)
        session1 = create_study_session(test_student, '2022-04-09', 'testloc', test_course)
        session2 = create_study_session(test_student, '2022-04-10', 'test2loc', test_course)
        response = self.client.get(reverse('study:sessions'))

        #Queryset is not ordered or a list so ordered = False for this to work
        self.assertQuerysetEqual(response.context['sessions_list'], [session1, session2], ordered = False) 

class SessionRemoveTests(TestCase):
    def test_no_session_to_remove(self):
        """
        if no sessions are available then show a message
        """
        user = create_user()
        self.client.force_login(user)
        test_student = create_student(user, 'testfirstname', 'testlastname', 'testcid', 'testpref', int(1), 'test bio')
        test_course = create_course("CS", "3240", "Test Course")
        test_course.roster.add(test_student)
        response = self.client.get(reverse('study:remove-session'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have not added any sessions yet! Go and add some and then come back here to remove a session if needed!")
        self.assertQuerysetEqual(response.context['remove_sessions_list'], [])

    def test_remove_one_session(self):
        
        """
        if a session is available you can remove it
        """
        user = create_user()
        self.client.force_login(user)
        test_student = create_student(user, 'testfirstname', 'testlastname', 'testcid', 'testpref', int(1), 'test bio')
        test_course = create_course("CS", "3240", "Test Course")
        test_course.roster.add(test_student)
        session1 = create_study_session(test_student, '2022-04-09', 'testloc', test_course)
        self.client.post(reverse('study:removeSession'), {'removeSession' : session1.id})
        response = self.client.get(reverse('study:remove-session'))

        self.assertQuerysetEqual(response.context['remove_sessions_list'], [])



