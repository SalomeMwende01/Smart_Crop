from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Field, FieldStage, FieldStatus


class FieldModelStatusTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='Pass1234!', role=User.Role.ADMIN)
        self.agent = User.objects.create_user(username='agent', password='Pass1234!', role=User.Role.AGENT)

    def test_completed_status_when_harvested(self):
        field = Field.objects.create(
            name='West Block',
            crop_type='Corn',
            planting_date=timezone.localdate() - timedelta(days=90),
            current_stage=FieldStage.HARVESTED,
            assigned_agent=self.agent,
            created_by=self.admin,
        )

        self.assertEqual(field.computed_status, FieldStatus.COMPLETED)

    def test_at_risk_status_when_planted_too_long(self):
        field = Field.objects.create(
            name='North Block',
            crop_type='Beans',
            planting_date=timezone.localdate() - timedelta(days=20),
            current_stage=FieldStage.PLANTED,
            assigned_agent=self.agent,
            created_by=self.admin,
        )

        self.assertEqual(field.computed_status, FieldStatus.AT_RISK)


class FieldApiVisibilityTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='Pass1234!', role=User.Role.ADMIN)
        self.agent_one = User.objects.create_user(username='agent1', password='Pass1234!', role=User.Role.AGENT)
        self.agent_two = User.objects.create_user(username='agent2', password='Pass1234!', role=User.Role.AGENT)

        Field.objects.create(
            name='Field A',
            crop_type='Maize',
            planting_date=timezone.localdate() - timedelta(days=12),
            current_stage=FieldStage.GROWING,
            assigned_agent=self.agent_one,
            created_by=self.admin,
        )
        Field.objects.create(
            name='Field B',
            crop_type='Wheat',
            planting_date=timezone.localdate() - timedelta(days=15),
            current_stage=FieldStage.GROWING,
            assigned_agent=self.agent_two,
            created_by=self.admin,
        )

    def test_agent_only_lists_assigned_fields(self):
        token = Token.objects.create(user=self.agent_one)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.get(reverse('field-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Field A')
