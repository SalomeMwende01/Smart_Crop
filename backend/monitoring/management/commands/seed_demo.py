from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from monitoring.models import Field, FieldStage, FieldUpdate


class Command(BaseCommand):
    help = 'Create demo users, fields, and updates for the FieldPulse assessment.'

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            username='coordinator',
            defaults={
                'email': 'coordinator@fieldpulse.local',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        admin.set_password('Pass1234!')
        admin.role = User.Role.ADMIN
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        agent_one, _ = User.objects.get_or_create(
            username='agent_rose',
            defaults={'email': 'rose@fieldpulse.local', 'role': User.Role.AGENT},
        )
        agent_one.set_password('Pass1234!')
        agent_one.role = User.Role.AGENT
        agent_one.save()

        agent_two, _ = User.objects.get_or_create(
            username='agent_karim',
            defaults={'email': 'karim@fieldpulse.local', 'role': User.Role.AGENT},
        )
        agent_two.set_password('Pass1234!')
        agent_two.role = User.Role.AGENT
        agent_two.save()

        today = timezone.localdate()

        maize_field, _ = Field.objects.get_or_create(
            name='North Plot A',
            defaults={
                'crop_type': 'Maize',
                'planting_date': today - timedelta(days=20),
                'current_stage': FieldStage.GROWING,
                'assigned_agent': agent_one,
                'created_by': admin,
            },
        )

        beans_field, _ = Field.objects.get_or_create(
            name='River Edge B',
            defaults={
                'crop_type': 'Beans',
                'planting_date': today - timedelta(days=8),
                'current_stage': FieldStage.PLANTED,
                'assigned_agent': agent_two,
                'created_by': admin,
            },
        )

        FieldUpdate.objects.get_or_create(
            field=maize_field,
            stage=FieldStage.GROWING,
            note='Crop canopy increasing; irrigation stable.',
            created_by=agent_one,
        )

        FieldUpdate.objects.get_or_create(
            field=beans_field,
            stage=FieldStage.PLANTED,
            note='Germination visible in 65% of section.',
            created_by=agent_two,
        )

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
        self.stdout.write('Admin: coordinator / Pass1234!')
        self.stdout.write('Agent 1: agent_rose / Pass1234!')
        self.stdout.write('Agent 2: agent_karim / Pass1234!')
