from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from arkav_is_api.competition.models import Competition, Team, TeamMember, Task, TaskResponse, TaskCategory, TaskWidget


class CompetitionModelsTests(TestCase):
    def setUp(self):
        self.competition_cp = Competition.objects.create(
            name='Competitive Programming')
        self.competition_ctf = Competition.objects.create(
            name='Capture the Flag', max_team_members=3)
        self.competition_without_stages = Competition.objects.create(name='Empty')

        self.cp_stage_final = self.competition_cp.stages.create(name='CP Final', order=3)
        self.cp_stage_qualification = self.competition_cp.stages.create(name='CP Qualification', order=2)
        self.cp_stage_registration = self.competition_cp.stages.create(name='CP Registration', order=1)

        self.ctf_stage_registration = self.competition_ctf.stages.create(name='CTF Registration', order=1)
        self.ctf_stage_contest = self.competition_ctf.stages.create(name='CTF Contest', order=2)
        self.ctf_empty_stage = self.competition_ctf.stages.create(name='CTF Empty', order=99)

        self.user1 = User.objects.create_user(username='user1')
        self.user2 = User.objects.create_user(username='user2')
        self.user3 = User.objects.create_user(username='user3')
        self.user4 = User.objects.create_user(username='user4')

        self.ctf_team1 = Team.objects.create(name='ctf1', competition=self.competition_ctf)
        TeamMember.objects.create(team=self.ctf_team1, user=self.user2, is_approved=True)
        TeamMember.objects.create(team=self.ctf_team1, user=self.user3, is_approved=False)
        TeamMember.objects.create(team=self.ctf_team1, user=self.user1, is_approved=False)

        self.ctf_team2 = Team.objects.create(name='ctf2', competition=self.competition_ctf)
        TeamMember.objects.create(team=self.ctf_team2, user=self.user1, is_approved=True)
        TeamMember.objects.create(team=self.ctf_team2, user=self.user2, is_approved=True)
        TeamMember.objects.create(team=self.ctf_team2, user=self.user4, is_approved=True)

        self.category_documents = TaskCategory.objects.create(name='Documents')
        self.category_payment = TaskCategory.objects.create(name='Payment')
        self.widget_text = TaskWidget.objects.create(name='Text')
        self.widget_file = TaskWidget.objects.create(name='File')

        self.ctf_upload_ktm_task = Task.objects.create(
            name='Upload KTM',
            stage=self.ctf_stage_registration,
            category=self.category_documents,
            widget=self.widget_file,
            requires_validation=True,
        )
        self.ctf_upload_proof_of_payment = Task.objects.create(
            name='Upload proof of payment',
            stage=self.ctf_stage_registration,
            category=self.category_payment,
            widget=self.widget_file,
            requires_validation=True,
        )
        self.ctf_enter_shirt_sizes = Task.objects.create(
            name='Shirt sizes',
            stage=self.ctf_stage_registration,
            category=self.category_documents,
            widget=self.widget_text,
        )

        self.ctf_upload_writeup = Task.objects.create(
            name='Upload writeup',
            stage=self.ctf_stage_contest,
            category=self.category_documents,
            widget=self.widget_file,
            requires_validation=True,
        )

    def test_team_defaults(self):
        new_cpteam = Team.objects.create(name='New CP Team', competition=self.competition_cp)
        self.assertEqual(len(new_cpteam.secret_code), 6)
        self.assertEqual(new_cpteam.members.count(), 0)
        self.assertEqual(new_cpteam.approved_members.count(), 0)
        self.assertEqual(new_cpteam.pending_members.count(), 0)
        self.assertEqual(new_cpteam.active_stage.name, 'CP Registration')

    def test_team_override_defaults(self):
        new_ctfteam = Team.objects.create(
            name='New CTF Team',
            competition=self.competition_ctf,
            secret_code='overridencode',
            active_stage=self.ctf_stage_contest
        )
        self.assertEqual(new_ctfteam.secret_code, 'overridencode')
        self.assertEqual(new_ctfteam.members.count(), 0)
        self.assertEqual(new_ctfteam.approved_members.count(), 0)
        self.assertEqual(new_ctfteam.pending_members.count(), 0)
        self.assertEqual(new_ctfteam.active_stage.name, 'CTF Contest')

    def test_edit_team(self):
        '''
        Ensure manual defaults for active_stage does not mess up team instance editing.
        '''
        self.ctf_team2.name = 'edited ctf2'
        self.ctf_team2.save()
        self.assertEqual(self.ctf_team2.active_stage, self.ctf_stage_registration)
        self.ctf_team2.active_stage = self.ctf_stage_contest
        self.ctf_team2.save()
        self.assertEqual(self.ctf_team2.active_stage, self.ctf_stage_contest)

    def test_create_team_without_competition(self):
        try:
            Team.objects.create(name='fail')
            self.fail(msg='Team creation should fail if not given a competition.')
        except ValueError:
            pass

    def test_create_team_with_stageless_competition(self):
        try:
            Team.objects.create(name='fail', competition=self.competition_without_stages)
            self.fail(msg='Team creation should fail if given a competition without any stage.')
        except ValueError:
            pass

    def test_enforce_team_name_uniqueness(self):
        try:
            Team.objects.create(name='notunique', competition=self.competition_cp)
            Team.objects.create(name='notunique', competition=self.competition_ctf)
            self.fail(msg='Team name uniqueness must be enforced, even across competitions.')
        except IntegrityError:
            pass

    def test_enforce_team_secret_code_uniqueness(self):
        try:
            Team.objects.create(name='codenotunique', competition=self.competition_cp, secret_code='samesame')
            Team.objects.create(name='codenotunique', competition=self.competition_ctf, secret_code='samesame')
            self.fail(msg='Team secret code uniqueness must be enforced, even across competitions.')
        except IntegrityError:
            pass

    def test_team_get_approved_members(self):
        self.assertEqual(self.ctf_team1.approved_members.count(), 1)
        self.assertIn(self.user2, self.ctf_team1.approved_members)

        self.assertEqual(self.ctf_team2.approved_members.count(), 3)
        self.assertIn(self.user1, self.ctf_team2.approved_members)
        self.assertIn(self.user2, self.ctf_team2.approved_members)
        self.assertIn(self.user4, self.ctf_team2.approved_members)

    def test_team_get_pending_members(self):
        self.assertEqual(self.ctf_team1.pending_members.count(), 2)
        self.assertIn(self.user1, self.ctf_team1.pending_members)
        self.assertIn(self.user3, self.ctf_team1.pending_members)

        self.assertEqual(self.ctf_team2.pending_members.count(), 0)

    def test_task_response_default_state(self):
        # Create task response for a task that requires validation
        task_response_1 = TaskResponse.objects.create(team=self.ctf_team1, task=self.ctf_upload_ktm_task)
        self.assertEqual(task_response_1.status, TaskResponse.AWAITING_VALIDATION)

        # Create task response for a task that don't require validation
        task_response_2 = TaskResponse.objects.create(team=self.ctf_team1, task=self.ctf_enter_shirt_sizes)
        self.assertEqual(task_response_2.status, TaskResponse.COMPLETED)

    def test_task_response_override_defaults(self):
        # Create task response for a task that requires validation
        # Ensure defaults don't mess with manual status override
        task_response_1 = TaskResponse.objects.create(
            team=self.ctf_team1, task=self.ctf_upload_ktm_task, status=TaskResponse.COMPLETED)
        self.assertEqual(task_response_1.status, TaskResponse.COMPLETED)

    def test_edit_task_response(self):
        task_response_1 = TaskResponse.objects.create(team=self.ctf_team1, task=self.ctf_upload_ktm_task)
        self.assertEqual(task_response_1.status, TaskResponse.AWAITING_VALIDATION)

        # Note: status changes are to be handled at the view level
        # The TaskResponse model is only responsible for assigning default statuses
        task_response_1.response = 'testresponse1'
        task_response_1.save()
        self.assertEqual(task_response_1.response, 'testresponse1')
        self.assertEqual(task_response_1.status, TaskResponse.AWAITING_VALIDATION)

        task_response_1.status = TaskResponse.COMPLETED
        task_response_1.save()
        self.assertEqual(task_response_1.response, 'testresponse1')
        self.assertEqual(task_response_1.status, TaskResponse.COMPLETED)

        task_response_1.status = TaskResponse.AWAITING_VALIDATION
        task_response_1.save()
        self.assertEqual(task_response_1.response, 'testresponse1')
        self.assertEqual(task_response_1.status, TaskResponse.AWAITING_VALIDATION)

        task_response_1.status = TaskResponse.REJECTED
        task_response_1.save()
        self.assertEqual(task_response_1.response, 'testresponse1')
        self.assertEqual(task_response_1.status, TaskResponse.REJECTED)

        task_response_2 = TaskResponse.objects.create(team=self.ctf_team2, task=self.ctf_enter_shirt_sizes)
        self.assertEqual(task_response_2.status, TaskResponse.COMPLETED)

        # Note: status changes are to be handled at the view level
        # The TaskResponse model is only responsible for assigning default statuses
        task_response_2.response = 'testresponse2'
        task_response_2.save()
        self.assertEqual(task_response_2.response, 'testresponse2')
        self.assertEqual(task_response_2.status, TaskResponse.COMPLETED)

        task_response_2.status = TaskResponse.REJECTED
        task_response_2.save()
        self.assertEqual(task_response_2.response, 'testresponse2')
        self.assertEqual(task_response_2.status, TaskResponse.REJECTED)

    def test_team_has_completed_active_stage(self):
        self.assertFalse(self.ctf_team1.has_completed_active_stage)
        self.assertFalse(self.ctf_team2.has_completed_active_stage)

        task_response_1 = TaskResponse.objects.create(team=self.ctf_team1, task=self.ctf_upload_ktm_task)
        task_response_2 = TaskResponse.objects.create(team=self.ctf_team1, task=self.ctf_upload_proof_of_payment)
        task_response_3 = TaskResponse.objects.create(team=self.ctf_team1, task=self.ctf_enter_shirt_sizes)
        self.assertFalse(self.ctf_team1.has_completed_active_stage)

        task_response_1.status = TaskResponse.COMPLETED
        task_response_1.save()
        task_response_2.status = TaskResponse.REJECTED
        task_response_2.save()
        self.assertFalse(self.ctf_team1.has_completed_active_stage)
        self.assertFalse(self.ctf_team2.has_completed_active_stage)

        task_response_2.status = TaskResponse.COMPLETED
        task_response_2.save()
        self.assertTrue(self.ctf_team1.has_completed_active_stage)
        self.assertFalse(self.ctf_team2.has_completed_active_stage)

        # An stage with no tasks is by definition completed
        self.ctf_team1.active_stage = self.ctf_empty_stage
        self.ctf_team1.save()
        self.assertTrue(self.ctf_team1.has_completed_active_stage)

        self.ctf_team1.active_stage = self.ctf_stage_contest
        self.ctf_team1.save()
        self.assertFalse(self.ctf_team1.has_completed_active_stage)

        task_response_4 = TaskResponse.objects.create(team=self.ctf_team1, task=self.ctf_upload_writeup)
        task_response_4.status = TaskResponse.COMPLETED
        task_response_4.save()
        self.assertTrue(self.ctf_team1.has_completed_active_stage)

        # has_completed_active_stage should not core about the completeness of tasks
        # in stages other than the active stage
        task_response_2.status = TaskResponse.REJECTED
        task_response_2.save()
        self.assertTrue(self.ctf_team1.has_completed_active_stage)
