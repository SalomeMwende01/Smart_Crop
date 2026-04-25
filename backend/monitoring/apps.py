from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'
    verbose_name = 'Monitoring'

    def ready(self):
        # Auto-seed demo data on first migrate (for Render free tier)
        from django.db.models.signals import post_migrate
        from django.contrib.auth import get_user_model
        from django.utils import timezone
        from datetime import timedelta
        import os

        def seed_demo_data(sender, **kwargs):
            User = get_user_model()
            from accounts.models import User as AccountUser
            from monitoring.models import Field, FieldUpdate, FieldStage

            # Skip if already seeded (check for existing users)
            if User.objects.filter(username='coordinator').exists():
                return

            # Create Admin Coordinator
            admin, _ = User.objects.get_or_create(
                username='coordinator',
                defaults={
                    'email': 'coordinator@fieldpulse.local',
                    'role': AccountUser.Role.ADMIN,
                    'is_staff': True,
                    'is_superuser': True,
                },
            )
            admin.set_password('Pass1234!')
            admin.role = AccountUser.Role.ADMIN
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

            # Create Field Agents
            for username, email in [('agent_rose', 'rose@fieldpulse.local'), ('agent_karim', 'karim@fieldpulse.local')]:
                user, _ = User.objects.get_or_create(
                    username=username,
                    defaults={'email': email, 'role': AccountUser.Role.AGENT},
                )
                user.set_password('Pass1234!')
                user.role = AccountUser.Role.AGENT
                user.save()

            agent_one = User.objects.get(username='agent_rose')
            agent_two = User.objects.get(username='agent_karim')
            admin = User.objects.get(username='coordinator')

            # Create sample fields
            today = timezone.localdate()

            Field.objects.get_or_create(
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
                field=beans_field,
                stage=FieldStage.PLANTED,
                note='Germination visible in 65% of section.',
                created_by=agent_two,
            )

        # Connect signal - will trigger on render's migrate
        from django.conf import settings
        if getattr(settings, 'RENDER_DEPLOYMENT', False) or os.getenv('RENDER', '') == 'true':
            post_migrate.connect(seed_demo_data, sender=self)
