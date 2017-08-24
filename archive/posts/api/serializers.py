from rest_framework.serializers import ModelSerializer

from ..models import Post


class PostListSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "pk", "slug", "title", "body",
        ]


class PostDetailSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
             "pk", "slug", "title", "body", "created", "modified", "author",
        ]


class PostUpdateCreateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
             "title", "body", "publish_on",
        ]
