from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, HttpResponseRedirect

from .forms import CreateCommentForm
from .models import Comment
# Create your views here.


def reply(request, comment):
    comment = Comment.objects.get(id=int(comment))
    parent = comment

    if comment.parent:
        parent = comment.parent

    form = None

    if request.user.is_authenticated():
        initial = {
            "content_type": comment.content_type,
            "object_id": comment.object_id,
        }
        form = CreateCommentForm(request.POST or None, initial=initial)
        if form.is_valid():
            form_content_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=form_content_type)
            form_object_id = form.cleaned_data.get("object_id")
            form_comment = form.cleaned_data.get("comment_body")
            parent = comment

            comment, created = Comment.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=form_object_id,
                body=form_comment,
                parent=parent,
            )
            return HttpResponseRedirect(comment.get_absolute_url())

    context = {
        "comment": parent,
        "form": form,
    }
    return render(request, "replies.html", context)


def thread(request, content, pk):
    content_type = ContentType.objects.get(model=content)
    object_id = pk
    instance = content_type.model_class().objects.get(id=int(pk))
    comments = Comment.objects.filter(content_type=content_type, object_id=object_id)
    form = None

    if request.user.is_authenticated():
        initial = {
            "content_type": content_type,
            "object_id": object_id,
        }
        form = CreateCommentForm(request.POST or None, initial=initial)
        if form.is_valid():
            form_content_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=form_content_type)
            form_object_id = form.cleaned_data.get("object_id")
            form_comment = form.cleaned_data.get("comment_body")
            comment_id = str(request.POST.get("comment_id"))
            try:
                comment_instance = Comment.objects.get(id=comment_id)
                parent = comment_instance
            except:
                parent = None

            comment, created = Comment.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=form_object_id,
                body=form_comment,
                parent=parent,
            )
            return HttpResponseRedirect(comment.get_absolute_url())

    context = {
        "comments": comments,
        "instance": instance,
        "form": form,
    }
    return render(request, "comments.html", context)
