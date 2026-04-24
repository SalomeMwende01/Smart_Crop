from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        AGENT = 'AGENT', 'Field Agent'

    role = models.CharField(max_length=16, choices=Role.choices, default=Role.AGENT)

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_agent_role(self):
        return self.role == self.Role.AGENT
