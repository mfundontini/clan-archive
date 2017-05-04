from __future__ import unicode_literals

import random

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify


def upload_to(instance, filename):
    filename = filename.split(".")
    filename = "%s_%s_%s.%s" % (filename[0], instance.id, random.randrange(100), filename[1])
    return filename


class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_to, height_field="height", width_field="width")
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    author = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return "%s by %s" % (self.title, self.author)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

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
            index = qs.last() + 1
            slug = "%s-%s" % (instance.title, index)
            slug = slugify(slug)
            instance.slug = slug
        else:
            slug = "%s-1" % instance.title
            instance.slug = slug

pre_save.connect(receiver=pre_save_slug_modify, sender=Post)
