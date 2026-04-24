from django.db import transaction
from rest_framework import serializers

from accounts.models import User

from .models import Field, FieldStatus, FieldUpdate


class AssignedAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class FieldSerializer(serializers.ModelSerializer):
    assigned_agent = AssignedAgentSerializer(read_only=True)
    assigned_agent_id = serializers.PrimaryKeyRelatedField(
        source='assigned_agent',
        queryset=User.objects.filter(role=User.Role.AGENT),
        write_only=True,
        required=False,
        allow_null=True,
    )
    computed_status = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = [
            'id',
            'name',
            'crop_type',
            'planting_date',
            'current_stage',
            'computed_status',
            'assigned_agent',
            'assigned_agent_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'computed_status']

    def get_computed_status(self, obj):
        status = obj.computed_status
        return {'code': status, 'label': FieldStatus(status).label}


class FieldUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = FieldUpdate
        fields = ['id', 'field', 'stage', 'note', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def get_created_by(self, obj):
        return {
            'id': obj.created_by_id,
            'username': obj.created_by.username,
            'role': obj.created_by.role,
        }

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        validated_data['created_by'] = request.user

        update = super().create(validated_data)

        field = update.field
        field.current_stage = update.stage
        field.save(update_fields=['current_stage', 'updated_at'])

        return update
