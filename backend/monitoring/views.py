from collections import Counter

from django.db.models import Count
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User

from .models import Field, FieldStatus, FieldUpdate
from .permissions import IsAdminOrAssignedAgentReadOnly
from .serializers import FieldSerializer, FieldUpdateSerializer


class MonitoringHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'service': 'monitoring', 'status': 'ok'})


class FieldViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    permission_classes = [IsAdminOrAssignedAgentReadOnly]

    def get_queryset(self):
        base_qs = Field.objects.select_related('assigned_agent').all()

        if self.request.user.role == User.Role.ADMIN:
            return base_qs

        return base_qs.filter(assigned_agent=self.request.user)

    def _ensure_admin_write(self):
        if self.request.user.role != User.Role.ADMIN:
            raise PermissionDenied('Only admins can create or edit fields directly.')

    def perform_create(self, serializer):
        self._ensure_admin_write()
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        self._ensure_admin_write()
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        self._ensure_admin_write()
        return super().destroy(request, *args, **kwargs)


class FieldUpdateListCreateView(generics.ListCreateAPIView):
    serializer_class = FieldUpdateSerializer
    permission_classes = [IsAuthenticated]

    def _get_field(self):
        field = generics.get_object_or_404(Field, pk=self.kwargs['field_id'])

        user = self.request.user
        if user.role == User.Role.ADMIN:
            return field

        if user.role == User.Role.AGENT and field.assigned_agent_id == user.id:
            return field

        raise PermissionDenied('You do not have access to this field.')

    def get_queryset(self):
        field = self._get_field()
        return FieldUpdate.objects.filter(field=field).select_related('created_by')

    def perform_create(self, serializer):
        field = self._get_field()
        serializer.save(field=field)


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == User.Role.ADMIN:
            fields_qs = Field.objects.all()
        else:
            fields_qs = Field.objects.filter(assigned_agent=request.user)

        fields = list(fields_qs)

        status_counter = Counter(field.computed_status for field in fields)
        stage_breakdown = dict(fields_qs.values('current_stage').annotate(total=Count('id')).values_list('current_stage', 'total'))

        at_risk_fields = [
            {'id': field.id, 'name': field.name, 'crop_type': field.crop_type}
            for field in fields
            if field.computed_status == FieldStatus.AT_RISK
        ]

        return Response(
            {
                'total_fields': len(fields),
                'status_breakdown': {
                    'ACTIVE': status_counter.get(FieldStatus.ACTIVE, 0),
                    'AT_RISK': status_counter.get(FieldStatus.AT_RISK, 0),
                    'COMPLETED': status_counter.get(FieldStatus.COMPLETED, 0),
                },
                'stage_breakdown': stage_breakdown,
                'insights': {
                    'at_risk_count': status_counter.get(FieldStatus.AT_RISK, 0),
                    'at_risk_fields': at_risk_fields[:5],
                },
            },
            status=status.HTTP_200_OK,
        )
