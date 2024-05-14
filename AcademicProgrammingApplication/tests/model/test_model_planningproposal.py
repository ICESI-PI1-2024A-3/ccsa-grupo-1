from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from AcademicProgrammingApplication.models import PlanningProposal


class PlanningProposalModelTest(TestCase):

    def setUp(self):
        """
        Setting up initial conditions for each test.
        Creates a PlanningProposal object for testing.
        """
        self.planning_proposal = PlanningProposal.objects.create(
            username='test_user',
            name_file='test_file',
            date=date.today(),
            path=SimpleUploadedFile("test_file.xlsx", b"file_content",
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        )

    def test_planning_proposal_creation(self):
        """
        Test for PlanningProposal object creation.
        Verifies that the PlanningProposal object is created successfully.
        """
        self.assertEqual(PlanningProposal.objects.count(), 1)

    def test_planning_proposal_username(self):
        """
        Test for username field of PlanningProposal.
        Verifies that the username field is set correctly.
        """
        self.assertEqual(self.planning_proposal.username, 'test_user')

    def test_planning_proposal_name_file(self):
        """
        Test for name_file field of PlanningProposal.
        Verifies that the name_file field is set correctly.
        """
        self.assertEqual(self.planning_proposal.name_file, 'test_file')

    def test_planning_proposal_date(self):
        """
        Test for date field of PlanningProposal.
        Verifies that the date field is set correctly.
        """
        self.assertEqual(self.planning_proposal.date, date.today())

    def test_planning_proposal_path(self):
        """
        Test for path field of PlanningProposal.
        Verifies that the path field starts with 'files/'.
        """
        self.assertTrue(self.planning_proposal.path.name.startswith('files/'))

    def test_planning_proposal_str(self):
        """
        Test for __str__ method of PlanningProposal.
        Verifies that the __str__ method returns the name_file of the PlanningProposal.
        """
        self.assertEqual(str(self.planning_proposal), 'test_file')
