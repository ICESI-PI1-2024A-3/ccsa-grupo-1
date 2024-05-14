from django.test import TestCase
from django.utils import timezone
from AcademicProgrammingApplication.models import Contract, Teacher


class ContractModelTest(TestCase):
    def setUp(self):
        """
        Setting up initial conditions for each test.
        Creates a Teacher object and a Contract object for testing.
        """
        self.teacher = Teacher.objects.create(
            id='123456789',
            name='Profesor de Prueba',
            email='test@example.com',
            cellphone='1234567890',
            city='Ciudad de Prueba',
            state='ACTIVO',
            picture='picture.jpg'
        )

        self.contract = Contract.objects.create(
            contract_status='ACTIVO',
            contact_preparation_date=timezone.now().date(),
            id_teacher=self.teacher
        )

    def test_contract_creation(self):
        """
        Test for Contract object creation.
        Verifies that the Contract object is created successfully.
        """
        self.assertEqual(Contract.objects.count(), 1)

    def test_contract_status(self):
        """
        Test for contract status.
        Verifies that the contract status is set correctly.
        """
        self.assertEqual(self.contract.contract_status, 'ACTIVO')

    def test_contract_preparation_date(self):
        """
        Test for contract preparation date.
        Verifies that the contract preparation date is set correctly.
        """
        self.assertEqual(self.contract.contact_preparation_date, timezone.now().date())

    def test_contract_teacher_association(self):
        """
        Test for teacher association with contract.
        Verifies that the contract is associated with the correct teacher.
        """
        self.assertEqual(self.contract.id_teacher, self.teacher)
