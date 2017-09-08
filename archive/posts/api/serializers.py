from rest_framework.serializers import (
    ModelSerializer, HyperlinkedIdentityField,
    SerializerMethodField,
)

from ..models import Post


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="posts-api:detail",
        lookup_field="slug"
    )
    author = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "url", "pk", "slug", "title", "body", "author"
        ]

    def get_author(self, obj):
        if obj.author.first_name and obj.author.last_name:
            return "%s-%s" % (obj.author.first_name, obj.author.last_name)
        return obj.author.username


class PostDetailSerializer(ModelSerializer):
    image = SerializerMethodField()
    html = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
             "pk", "slug", "title", "body", "created", "modified", "author",
             "image", "html"
        ]

    def get_image(self, obj):
        try:
            image_url = obj.image.url
        except:
            image_url = None
        return image_url

    def get_html(self, obj):
        return obj.get_marked_content()

    def get_author(self, obj):
        if obj.author.first_name and obj.author.last_name:
            return "%s-%s" % (obj.author.first_name, obj.author.last_name)
        return obj.author.username


class PostUpdateCreateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
             "title", "body", "publish_on",
        ]
