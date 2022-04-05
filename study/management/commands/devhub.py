from django.core.management.base import BaseCommand, CommandError
from study.models import Course
from urllib.request import urlopen
import json, re

class Command(BaseCommand):
    help = 'Imports all courses from DevHub API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--term',
            default='2022 Spring',
            help='Term of courses to be imported (in format "YYYY Season")',
        )

        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all courses before importing',
        )

    def handle(self, *args, **options):
        if options['reset']:
            Course.objects.all().delete()
            if not Course.objects.all():
                self.stdout.write(self.style.SUCCESS('Successfully deleted all courses'))

        with urlopen("https://api.devhub.virginia.edu/v1/courses") as url:
            data = json.load(url)
            courses = set()
            for course in data['class_schedules']['records']:
                term = course[-1]
                subject = course[0]
                number = course[1]
                name = course[4]
                section = re.sub('[\W_]+', '', course[2]).lstrip('0')
                if term == options['term'] and (subject, number, name, section) not in courses:
                    courses.add((subject, number, name, section))
            for course in courses:
                Course.objects.create(subject=course[0], number=course[1], name=course[2], section=course[3])

        self.stdout.write(self.style.SUCCESS('Successfully imported courses'))
