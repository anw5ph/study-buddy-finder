from django.contrib.postgres.fields import ArrayField
from django.db import models
# from django_google_maps import fields as map_fields
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


# class Location(models.Model):
#     address = map_fields.AddressField(max_length=200)
#     geolocation = map_fields.GeoLocationField(max_length=100)

#     def __str__(self):
#         return self.address


class Student(models.Model):
    student_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=None)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    computing_id = models.CharField(max_length=7, default='')
    pref_name = models.CharField(max_length=30, default='')
    school_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)], default=1)
    bio = models.CharField(max_length=2600, default='')

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Course(models.Model):
    SUBJECT_CHOICES = [
        ('AAS', 'AAS'), ('ACCT', 'ACCT'), ('AFFL', 'AFFL'), ('AIRS', 'AIRS'), ('ALAR', 'ALAR'), ('AM', 'AM'), ('AMST', 'AMST'), ('ANTH', 'ANTH'), ('APMA', 'APMA'), ('ARAB', 'ARAB'), ('ARAD', 'ARAD'), ('ARAH', 'ARAH'), ('ARCH', 'ARCH'), ('ARCY', 'ARCY'), ('ARH', 'ARH'), ('ARTH', 'ARTH'), ('ARTR', 'ARTR'), ('ARTS', 'ARTS'), ('ASL', 'ASL'), ('ASTR', 'ASTR'), ('BIMS', 'BIMS'), ('BIOC', 'BIOC'), ('BIOL', 'BIOL'), ('BIOP', 'BIOP'), ('BME', 'BME'), ('BUS', 'BUS'), ('CASS', 'CASS'), ('CE', 'CE'), ('CELL', 'CELL'), ('CHE', 'CHE'), ('CHEM', 'CHEM'), ('CHIN', 'CHIN'), ('CHTR', 'CHTR'), ('CJ', 'CJ'), ('CLAS', 'CLAS'), ('COGS', 'COGS'), ('COLA', 'COLA'), ('COMM', 'COMM'), ('CONC', 'CONC'), ('CPE', 'CPE'), ('CREO', 'CREO'), ('CS', 'CS'), ('DANC', 'DANC'), ('DEM', 'DEM'), ('DH', 'DH'), ('DRAM', 'DRAM'), ('DS', 'DS'), ('EALC', 'EALC'), ('EAST', 'EAST'), ('ECE', 'ECE'), ('ECON', 'ECON'), ('EDHS', 'EDHS'), ('EDIS', 'EDIS'), ('EDLF', 'EDLF'), ('EDNC', 'EDNC'), ('EGMT', 'EGMT'), ('ELA', 'ELA'), ('ENCW', 'ENCW'), ('ENGL', 'ENGL'), ('ENGR', 'ENGR'), ('ENTP', 'ENTP'), ('ENWR', 'ENWR'), ('EP', 'EP'), ('ESL', 'ESL'), ('ETP', 'ETP'), ('EURS', 'EURS'), ('EVAT', 'EVAT'), ('EVEC', 'EVEC'), ('EVGE', 'EVGE'), ('EVHY', 'EVHY'), ('EVSC', 'EVSC'), ('FORU', 'FORU'), ('FREN', 'FREN'), ('FRTR', 'FRTR'), ('GBAC', 'GBAC'), ('GBUS', 'GBUS'), ('GCCS', 'GCCS'), ('GCNL', 'GCNL'), ('GCOM', 'GCOM'), ('GDS', 'GDS'), ('GERM', 'GERM'), ('GETR', 'GETR'), ('GHSS', 'GHSS'), ('GNUR', 'GNUR'), ('GREE', 'GREE'), ('GSAS', 'GSAS'), ('GSCI', 'GSCI'), ('GSGS', 'GSGS'), ('GSMS', 'GSMS'), ('GSSJ', 'GSSJ'), ('GSVS', 'GSVS'), ('HBIO', 'HBIO'), ('HEBR', 'HEBR'), ('HHE', 'HHE'), ('HIAF', 'HIAF'), ('HIEA', 'HIEA'), ('HIEU', 'HIEU'), ('HILA', 'HILA'), ('HIME', 'HIME'), ('HIND', 'HIND'), ('HISA', 'HISA'), ('HIST', 'HIST'), ('HIUS', 'HIUS'), ('HR', 'HR'), ('HSCI', 'HSCI'), ('HUMS', 'HUMS'), ('IMP', 'IMP'), ('INST', 'INST'), ('ISBU', 'ISBU'), ('ISCP', 'ISCP'), ('ISHU', 'ISHU'), ('ISIN',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         'ISIN'), ('ISLS', 'ISLS'), ('ISSS', 'ISSS'), ('IT', 'IT'), ('ITAL', 'ITAL'), ('ITTR', 'ITTR'), ('JAPN', 'JAPN'), ('JPTR', 'JPTR'), ('JWST', 'JWST'), ('KICH', 'KICH'), ('KINE', 'KINE'), ('KLPA', 'KLPA'), ('KOR', 'KOR'), ('KRTR', 'KRTR'), ('LAR', 'LAR'), ('LASE', 'LASE'), ('LAST', 'LAST'), ('LATI', 'LATI'), ('LAW', 'LAW'), ('LING', 'LING'), ('LNGS', 'LNGS'), ('LPPA', 'LPPA'), ('LPPL', 'LPPL'), ('LPPP', 'LPPP'), ('LPPS', 'LPPS'), ('MAE', 'MAE'), ('MATH', 'MATH'), ('MDST', 'MDST'), ('MED', 'MED'), ('MESA', 'MESA'), ('MEST', 'MEST'), ('MICR', 'MICR'), ('MISC', 'MISC'), ('MSE', 'MSE'), ('MSP', 'MSP'), ('MUBD', 'MUBD'), ('MUEN', 'MUEN'), ('MUPF', 'MUPF'), ('MUSI', 'MUSI'), ('NASC', 'NASC'), ('NCBM', 'NCBM'), ('NCCJ', 'NCCJ'), ('NCPR', 'NCPR'), ('NESC', 'NESC'), ('NUCO', 'NUCO'), ('NUIP', 'NUIP'), ('NURS', 'NURS'), ('PATH', 'PATH'), ('PC', 'PC'), ('PERS', 'PERS'), ('PETR', 'PETR'), ('PHAR', 'PHAR'), ('PHIL', 'PHIL'), ('PHS', 'PHS'), ('PHY', 'PHY'), ('PHYS', 'PHYS'), ('PLAC', 'PLAC'), ('PLAD', 'PLAD'), ('PLAN', 'PLAN'), ('PLAP', 'PLAP'), ('PLCP', 'PLCP'), ('PLIR', 'PLIR'), ('PLPT', 'PLPT'), ('POL', 'POL'), ('PORT', 'PORT'), ('POTR', 'POTR'), ('PPL', 'PPL'), ('PSCJ', 'PSCJ'), ('PSED', 'PSED'), ('PSHM', 'PSHM'), ('PSHP', 'PSHP'), ('PSLP', 'PSLP'), ('PSPA', 'PSPA'), ('PSPL', 'PSPL'), ('PSPM', 'PSPM'), ('PSPS', 'PSPS'), ('PST', 'PST'), ('PSTS', 'PSTS'), ('PSYC', 'PSYC'), ('RELA', 'RELA'), ('RELB', 'RELB'), ('RELC', 'RELC'), ('RELG', 'RELG'), ('RELH', 'RELH'), ('RELI', 'RELI'), ('RELJ', 'RELJ'), ('RELS', 'RELS'), ('RSC', 'RSC'), ('RUSS', 'RUSS'), ('RUTR', 'RUTR'), ('SANS', 'SANS'), ('SARC', 'SARC'), ('SAST', 'SAST'), ('SATR', 'SATR'), ('SEC', 'SEC'), ('SLAV', 'SLAV'), ('SLFK', 'SLFK'), ('SLTR', 'SLTR'), ('SOC', 'SOC'), ('SPAN', 'SPAN'), ('STAT', 'STAT'), ('STS', 'STS'), ('SWAH', 'SWAH'), ('SYS', 'SYS'), ('TURK', 'TURK'), ('UD', 'UD'), ('UNST', 'UNST'), ('URDU', 'URDU'), ('USEM', 'USEM'), ('VGRM', 'VGRM'), ('WGS', 'WGS'), ('ZFOR', 'ZFOR')
    ]
    subject = models.CharField(
        max_length=4, choices=SUBJECT_CHOICES, default='')
    number = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(9999)], default=0)
    name = models.CharField(max_length=100, default='')
    section = models.CharField(max_length=4, default='')
    # Use [Student object].courses.all() to see all of a student's courses
    roster = models.ManyToManyField(
        Student, blank=True, related_name="courses")

    def __str__(self):
        return f"{self.subject}, {self.number}, {self.name}"


class Study(models.Model):
    organizer = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField()
    # Use [Student object].studies.all() to see all of a student's study sessions
    attendees = models.ManyToManyField(Student, related_name="studies")
    location = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.study_subject + " " + self.study_number + " " + self.study_name
