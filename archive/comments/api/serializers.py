import json

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import Comment


class ListSerializer(ModelSerializer):
    parent = SerializerMethodField()
    children = SerializerMethodField()
    content = SerializerMethodField()
    content_id = SerializerMethodField()
    title = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["user", "body", "parent", "children", "content", "content_id", "title"]

    def get_parent(self, obj):
        if obj.is_parent:
            return None
        return obj.parent.body

    def get_children(self, obj):
        if obj.is_parent:
            children = []
            for child in obj.children:
                children.append(child.body)
            return children
        return None

    def get_content(self, obj):
        return obj.content_type.model_class().__name__

    def get_content_id(self, obj):
        return obj.object_id

    def get_title(self, obj):
        return str(obj.object_instance)

    def get_user(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return "%s-%s" % (obj.user.first_name, obj.user.last_name)
        return obj.user.username


class ChildSerializer(ModelSerializer):
    parent = SerializerMethodField()
    content = SerializerMethodField()
    content_id = SerializerMethodField()
    title = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["user", "body", "parent", "content", "content_id", "title"]

    def get_parent(self, obj):
        if obj.is_parent:
            return None
        return obj.parent.body

    def get_content(self, obj):
        return obj.content_type.model_class().__name__

    def get_content_id(self, obj):
        return obj.object_id

    def get_title(self, obj):
        return str(obj.object_instance)

    def get_user(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return "%s-%s" % (obj.user.first_name, obj.user.last_name)
        return obj.user.username
