import factory
import pytz
from .models import Semester, Subject, Program, Teacher, Class, Contract, Viatic, Student
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
from itertools import cycle
import random


class SemesterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Semester

    @staticmethod
    def generate_period():
        current_year = datetime.now().year
        semesters = []
        # Generate academic periods from 2020 to the current year
        for year in range(2020, current_year + 1):
            semesters.append(f'{year}-1')
            semesters.append(f'{year}-2')

        return semesters

    period = factory.Sequence(lambda n: SemesterFactory.generate_period()[n])

    @factory.lazy_attribute
    def start_date(self):
        # Assume the academic period starts in February for semester 1 and in August for semester 2
        year, semester = str(self.period).split('-')
        if semester == '1':
            return datetime(int(year), 2, 1)
        elif semester == '2':
            return datetime(int(year), 8, 1)

    @factory.lazy_attribute
    def ending_date(self):
        # Assume the academic period ends in June for semester 1 and in November for semester 2
        year, semester = str(self.period).split('-')
        if semester == '1':
            return datetime(int(year), 6, 30)
        elif semester == '2':
            return datetime(int(year), 11, 30)


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject

    # Generate fake data for subjects
    name = factory.Faker('sentence', nb_words=4)
    nrc = factory.Sequence(lambda n: f'NRC{n}')
    credits = factory.Faker('random_int', min=1, max=5)
    type = factory.Faker('random_element', elements=['CURRICULAR', 'ELECTIVA'])
    syllabus = factory.LazyAttribute(lambda _: SimpleUploadedFile('syllabus.pdf', b'pdf_content'))
    start_date = factory.Faker('date_between_dates', date_start=datetime(2024, 1, 1), date_end=datetime(2025, 6, 1))
    ending_date = factory.Faker('date_between_dates', date_start=factory.SelfAttribute('..start_date'), date_end=datetime(2025, 6, 1))
    modality = factory.Faker('random_element', elements=['PRESENCIAL', 'VIRTUAL'])
    num_sessions = factory.Faker('random_int', min=1, max=20)


# Names of programs
names = [
    "Especialización en Analítica aplicada a los negocios",
    "Maestría en Ciencias Administrativas",
    "Global MBA",
    "Maestría en Mercadeo",
    "Maestría en Finanzas",
    "Maestría en Economía",
    "Maestría en Finanzas Cuantitativas",
    "Doctorado en Ciencias Económicas y Administrativas",
]
random.shuffle(names)
names_iter = iter(names)


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Program

    # Generate fake data for programs
    name = factory.LazyFunction(lambda: next(names_iter))

    faculty = "Facultad de Ciencias Administrativas y Económicas"

    director = factory.Faker('name')
    cost = factory.Faker('random_int', min=8000000, max=40000000)

    @factory.lazy_attribute
    def type(self):
        # Determine program type based on name
        if "Especialización" in self.name:
            return "ESPECIALIZACIÓN"
        elif "Maestría" in self.name:
            return "MAESTRÍA"
        elif "Doctorado" in self.name:
            return "DOCTORADO"
        else:
            return random.choice(["ESPECIALIZACIÓN", "MAESTRÍA", "DOCTORADO"])

    modality = factory.Faker('random_element', elements=['PRESENCIAL', 'VIRTUAL'])

    @factory.lazy_attribute
    def duration(self):
        # Determine duration based on program type
        if self.type == "ESPECIALIZACIÓN":
            return random.randint(2, 4)  # (2-4 semesters)
        elif self.type == "MAESTRÍA":
            return random.randint(2, 6)  # (2-6 semesters)
        elif self.type == "DOCTORADO":
            return random.randint(6, 10)  # (6-10 semesters)
        else:
            return random.randint(2, 8)

    curriculum = factory.LazyAttribute(lambda _: SimpleUploadedFile(f'curriculum.pdf', b'pdf_content'))

    @factory.post_generation
    def semesters_and_subjects(self, create, extracted, **kwargs):
        if not create:
            # The call was to build an instance, not to create it.
            return

        if extracted:
            # Add extracted semesters and subjects.
            for semester in extracted['semesters']:
                self.semesters.add(semester)

            for subject in extracted['subjects']:
                self.subjects.add(subject)
        else:
            # Adds semesters and subjects from the database.
            semesters = Semester.objects.all()
            subjects = Subject.objects.all()
            self.semesters.add(*semesters)  # Associate all available semesters
            self.subjects.add(*random.sample(list(subjects), random.randint(2, 6)))  # Add between 2 and 6 subjects


def generate_random_date(start_date, end_date):
    """
    Función para generar una fecha aleatoria entre dos fechas dadas
    """
    # Calculate the difference between the dates
    delta = end_date - start_date
    # Generate a random number of days within the range
    random_days = random.randint(0, delta.days)
    # Add random days to the start date
    random_date = start_date + timedelta(days=random_days)
    return random_date


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    # Generate fake data for teachers
    id = factory.Sequence(lambda n: f'T{n}')
    name = factory.Faker('name')
    email = factory.Faker('email')
    cellphone = factory.Faker('phone_number')
    city = factory.Faker('city')
    state = factory.Faker('random_element', elements=['ACTIVO', 'INACTIVO'])
    picture = factory.LazyAttribute(lambda _: SimpleUploadedFile('picture.jpg', b'jpg_content'))

    # Create a contract with the same state as the teacher
    @factory.post_generation
    def create_contract(self, create, extracted, **kwargs):
        if not create:
            return
        # Define the start and end date for the generation of random dates
        date_start = datetime(2010, 1, 1)
        date_end = datetime(2024, 1, 1)
        # Generate a random date between date_start and date_end
        contact_preparation_date = generate_random_date(date_start, date_end)
        Contract.objects.create(
            id=f'Contract-{self.id}',
            contract_status=self.state,
            contact_preparation_date=contact_preparation_date,
            id_teacher=self
        )


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    # Generate fake data for students
    name = factory.Faker('name')
    student_id = factory.Sequence(lambda n: f'ST{n}')
    id_type = factory.Faker('random_element', elements=['CC', 'TI', 'CE'])  # Assuming Colombian ID types
    email = factory.Faker('email')


def round_to_nearest_half_hour(datetime_obj):
    """
    Auxiliary function to round a date to the nearest half hour
    """
    minutes = datetime_obj.minute
    if minutes < 30:
        datetime_obj = datetime_obj.replace(minute=0, second=0, microsecond=0)
    else:
        datetime_obj = datetime_obj.replace(minute=30, second=0, microsecond=0)
    return datetime_obj


class ClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Class

    # Generate fake data for classes
    id = factory.Sequence(lambda n: f'C{n}')

    @factory.lazy_attribute
    def start_date(self):
        # Generate a random date between January 1, 2024, and June 1, 2025
        start_of_year = datetime(2024, 1, 1, tzinfo=pytz.UTC)
        end_of_year = datetime(2025, 6, 1, tzinfo=pytz.UTC)
        random_date = start_of_year + timedelta(seconds=random.randint(0, int((end_of_year - start_of_year).total_seconds())))
        rounded_date = round_to_nearest_half_hour(random_date)
        return rounded_date

    @factory.lazy_attribute
    def ending_date(self):
        # Generate an end date that is 2 or 3 hours after the start date
        start_date = self.start_date
        duration = random.choice([timedelta(hours=2), timedelta(hours=3)])
        return start_date + duration
    
    modality = factory.Faker('random_element', elements=['PRESENCIAL', 'VIRTUAL'])
    classroom = factory.Faker('random_element',
                              elements=['Classroom A', 'Classroom B', 'Classroom C', 'Classroom D', 'Classroom E'])
    link = factory.Faker('url')
    send_email = factory.Faker('boolean')

    # Selecting an existing instance of Subject from the database
    subject = factory.LazyAttribute(lambda _: random.choice(Subject.objects.all()))

    # Selecting an existing Teacher instance from the database
    @factory.lazy_attribute
    def teacher(self):
        # Get a teacher that does not have overlapping classes during the new class' start and end dates
        teachers = Teacher.objects.exclude(
            class__start_date__range=(self.start_date, self.ending_date),
            class__ending_date__range=(self.start_date, self.ending_date)
        ).distinct()
        return random.choice(teachers)

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for student in extracted:
                self.students.add(student)
        else:
            students = Student.objects.all()
            self.students.add(
                *random.sample(list(students), random.randint(1, 10)))  # Add between 1 and 10 students to the class


class ViaticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Viatic

    # Generate fake data for viatics
    transport = factory.Faker('boolean')
    accommodation = factory.Faker('boolean')
    viatic = factory.Faker('boolean')
    id_teacher = factory.LazyAttribute(lambda _: random.choice(Teacher.objects.all()))