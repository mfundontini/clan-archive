from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from .models import Comment
# Create your views here.


def reply(request, comment):
    comment = Comment.objects.get(id=int(comment))
    parent = comment.parent
    context = {
        "comment": parent,
    }
    return render(request, "replies.html", context)


def thread(request, content, pk):
    content_type = ContentType.objects.get(model=content)
    object_id = pk
    instance = content_type.model_class().objects.get(id=int(pk))
    comments = Comment.objects.filter(content_type=content_type, object_id=object_id)
    context = {
        "comments": comments,
        "instance": instance,
    }
    return render(request, "comments.html", context)
