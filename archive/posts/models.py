from __future__ import unicode_literals

import random

from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils import timezone, safestring
from django.utils.text import slugify

from markdown_deux import markdown

from archive.comments.models import Comment


def upload_to(instance, filename):
    qs = Post.objects.all()
    instance_id = 1
    if qs.exists():
        instance_id = qs.first().id + 1
    filename = filename.split(".")
    filename = "%s_%s_%s.%s" % (filename[0], instance_id, random.randrange(100), filename[1])
    return filename


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish_on__lte=timezone.now())


class User(AbstractUser):
    pass


class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_to, height_field="height", width_field="width")
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish_on = models.DateField(auto_now=False, auto_now_add=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = PostManager()

    def __unicode__(self):
        return "%s by %s" % (self.title, self.author)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    def get_marked_content(self):
        content = markdown(self.body)
        marked = safestring.mark_safe(content)
        return marked

    @property
    def comments(self):
        qs = Comment.objects.filter_parents_by_instance(self)
        return qs

    @property
    def comment_count(self):
        number = self.comments.count()
        return number

    @property
    def content_type(self):
        c_type = ContentType.objects.get_for_model(self.__class__)
        return c_type

    class Meta:
        ordering = ["-created", "-modified"]


def pre_save_slug_modify(sender, instance, *args, **kwargs):
    if instance.id:
        slug = "%s-%s" % (instance.title, instance.id)
        slug = slugify(slug)
        instance.slug = slug
    else:
        qs = Post.objects.all()
        if qs.exists():
            index = qs.first().id + 1
            slug = "%s-%s" % (instance.title, index)
            slug = slugify(slug)
            instance.slug = slug
        else:
            slug = "%s-1" % instance.title
            slug = slugify(slug)
            instance.slug = slug

pre_save.connect(receiver=pre_save_slug_modify, sender=Post)
