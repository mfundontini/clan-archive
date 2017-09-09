from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import ListSerializer, ChildSerializer, DetailSerializer
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


class CommentDetailAPIView(RetrieveAPIView):
    serializer_class = DetailSerializer
    queryset = Comment.objects.all()
    lookup_field = "pk"

