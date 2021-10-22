from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *


class PermissionMixin:
    def get_permission(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        return [persmission() for permission in permissions]


class ProblemViewSet(PermissionMixin, ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]