import factory
from .models import Semester, Subject, Program, Teacher, Class, Contract, Viatic, Student
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
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
    start_date = factory.Faker('date')
    ending_date = factory.Faker('date')
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


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    # Generate fake data for students
    name = factory.Faker('name')
    student_id = factory.Sequence(lambda n: f'ST{n}')
    id_type = factory.Faker('random_element', elements=['CC', 'TI', 'CE'])  # Assuming Colombian ID types
    email = factory.Faker('email')


class ClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Class

    # Generate fake data for classes
    id = factory.Sequence(lambda n: f'C{n}')
    start_date = factory.Faker('date_time', tzinfo=datetime.now().astimezone().tzinfo)
    ending_date = factory.Faker('date_time', tzinfo=datetime.now().astimezone().tzinfo)
    modality = factory.Faker('random_element', elements=['PRESENCIAL', 'VIRTUAL'])
    classroom = factory.Faker('random_element',
                              elements=['Classroom A', 'Classroom B', 'Classroom C', 'Classroom D', 'Classroom E'])
    link = factory.Faker('url')
    send_email = factory.Faker('boolean')

    # Selecting an existing instance of Subject from the database
    subject = factory.LazyAttribute(lambda _: random.choice(Subject.objects.all()))

    # Selecting an existing Teacher instance from the database
    teacher = factory.LazyAttribute(lambda _: random.choice(Teacher.objects.all()))

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


teacher_cycle = cycle(Teacher.objects.all())


class ContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract

    # Generate fake data for contracts
    contract_status = factory.Faker('random_element', elements=['ACTIVO', 'INACTIVO'])
    contact_preparation_date = factory.Faker('date')
    id_teacher = factory.LazyAttribute(lambda _: next(teacher_cycle))


class ViaticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Viatic

    # Generate fake data for viatics
    transport = factory.Faker('boolean')
    accommodation = factory.Faker('boolean')
    viatic = factory.Faker('boolean')
    id_teacher = factory.LazyAttribute(lambda _: random.choice(Teacher.objects.all()))


