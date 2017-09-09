from rest_framework.generics import ListAPIView

from .serializers import ListSerializer, ChildSerializer
from ..models import Comment


class CommentListAPIView(ListAPIView):
    serializer_class = ListSerializer

    def get_queryset(self):
        return Comment.objects.all()


class ParentListAPIView(ListAPIView):
    serializer_class = ListSerializer

    def get_queryset(self):
        return Comment.objects.filter_parents()


class ChildrenListAPIView(ListAPIView):
    serializer_class = ChildSerializer

    def get_queryset(self):
        return Comment.objects.filter_children()
