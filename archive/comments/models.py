from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CommentManager(models.Manager):
    def filter_by_instance(self, instance, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super(CommentManager, self).filter(content_type=content_type, object_id=object_id)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_instance = GenericForeignKey("content_type", "object_id")

    objects = CommentManager()

    def __unicode__(self):
        return str(self.user.username)
