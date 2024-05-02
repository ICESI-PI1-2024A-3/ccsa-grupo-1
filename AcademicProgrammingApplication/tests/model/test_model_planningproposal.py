from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from AcademicProgrammingApplication.models import PlanningProposal

class PlanningProposalModelTest(TestCase):
    def setUp(self):
        self.planning_proposal = PlanningProposal.objects.create(
            username='test_user',
            name_file='test_file',
            date=date.today(),
            path=SimpleUploadedFile("test_file.xlsx", b"file_content", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        )

    def test_planning_proposal_creation(self):
        self.assertEqual(PlanningProposal.objects.count(), 1)

    def test_planning_proposal_username(self):
        self.assertEqual(self.planning_proposal.username, 'test_user')

    def test_planning_proposal_name_file(self):
        self.assertEqual(self.planning_proposal.name_file, 'test_file')

    def test_planning_proposal_date(self):
        self.assertEqual(self.planning_proposal.date, date.today())

    def test_planning_proposal_path(self):
        self.assertTrue(self.planning_proposal.path.name.startswith('files/'))

    def test_planning_proposal_str(self):
        self.assertEqual(str(self.planning_proposal), 'test_file')