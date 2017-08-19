from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.urlresolvers import reverse


class CommentManager(models.Manager):
    def filter_parents_by_instance(self, instance, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super(CommentManager, self).filter(content_type=content_type, object_id=object_id).filter(parent__isnull=True)

    def filter_by_instance(self, instance, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super(CommentManager, self).filter(content_type=content_type, object_id=object_id)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_instance = GenericForeignKey("content_type", "object_id")

    objects = CommentManager()

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def children(self):
        if self.is_parent:
            qs = Comment.objects.filter(parent=self)
            return qs
        return None

    def __unicode__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        instance = self.content_type.model_class().objects.get(id=self.object_id).id
        if self.is_parent:
            # return thread
            return reverse("comments:thread", kwargs={"content": "post", "pk": instance})
        # return reply
        return reverse("comments:reply", kwargs={"comment": self.pk})
