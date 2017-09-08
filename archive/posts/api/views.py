from django.db.models import Q
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from ..models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostUpdateCreateSerializer
from .permissions import IsOwnerOrSuperUser


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny, ]

    # ugly search for test reasons
    def get_queryset(self):
        queryset = Post.objects.all()
        search = self.request.GET.get("q")
        if search:
            queryset = Post.objects.all().filter(
                Q(title__icontains=search) |
                Q(body__icontains=search) |
                Q(author__username__icontains=search) |
                Q(author__first_name__icontains=search)
            )
        return queryset


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny, ]


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrSuperUser, ]


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsOwnerOrSuperUser, ]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

