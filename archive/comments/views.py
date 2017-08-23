import json

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from .forms import CreateCommentForm
from .models import Comment
from .utils import make_new_form
# I left the function based views uncommented out, even though they are ot used, for future reference


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


class CommentThreadView(TemplateView):
    template_name = "comments.html"
    partial_template = "comments_partial.html"

    def get(self, *args, **kwargs):
        content = kwargs.get("content")
        self.object_id = int(kwargs.get("pk"))
        self.content_type = ContentType.objects.get(model=content)
        self.instance = self.content_type.model_class().objects.get(id=self.object_id)
        self.comments = Comment.objects.filter(content_type=self.content_type, object_id=self.object_id)
        context = self.get_context_data(obj_id=self.object_id, c_type=self.content_type, **kwargs)
        if self.request.is_ajax():
            html = render_to_string("comments_partial.html", context=context, request=self.request)
            serialized_data = json.dumps({"html": html})
            return HttpResponse(serialized_data, content_type="application/json")
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        form = CreateCommentForm(self.request.POST)
        if form.is_valid():
            form_content_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=form_content_type)
            form_object_id = form.cleaned_data.get("object_id")
            form_comment = form.cleaned_data.get("comment_body")
            comment_id = str(self.request.POST.get("comment_id"))
            try:
                comment_instance = Comment.objects.get(id=comment_id)
                parent = comment_instance
            except:
                parent = None

            comment, created = Comment.objects.get_or_create(
                user=self.request.user,
                content_type=content_type,
                object_id=form_object_id,
                body=form_comment,
                parent=parent,
            )
            if self.request.is_ajax():
                comments = Comment.objects.filter(content_type=content_type, object_id=form_object_id)
                instance = content_type.model_class().objects.get(id=form_object_id)
                new_form = make_new_form(self.request, form_object_id, content_type)
                context = {
                    "form": new_form,
                    "comments": comments,
                    "instance": instance,
                }
                html = render_to_string("comments_partial.html", context=context, request=self.request)
                serialized_data = json.dumps({"html": html})
                return HttpResponse(serialized_data, content_type="application/json")
            return HttpResponseRedirect(comment.get_absolute_url())

    def get_context_data(self, obj_id=None, c_type=None, **kwargs):
        super(CommentThreadView, self).get_context_data(**kwargs)
        form = make_new_form(self.request, obj_id=obj_id, c_type=c_type)
        context = {
            "comments": self.comments,
            "instance": self.instance,
            "form": form,
        }

        return context


class CommentReplyView(TemplateView):
    template_name = "replies.html"
    partial_template = "comments_partial.html"

    def get(self, *args, **kwargs):
        comment = int(kwargs.get("comment"))
        self.comment_instance = Comment.objects.get(id=comment)
        self.parent = self.comment_instance
        if self.comment_instance.parent:
            self.parent = self.comment_instance.parent
        context = self.get_context_data(object_pk=self.comment_instance.object_id, content_type=self.comment_instance.content_type, **kwargs)
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        form = CreateCommentForm(self.request.POST)
        if form.is_valid():
            form_content_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=form_content_type)
            form_object_id = form.cleaned_data.get("object_id")
            form_comment = form.cleaned_data.get("comment_body")
            comment_id = str(self.request.POST.get("comment_id"))
            try:
                comment_instance = Comment.objects.get(id=comment_id)
                parent = comment_instance
            except:
                parent = None

            comment, created = Comment.objects.get_or_create(
                user=self.request.user,
                content_type=content_type,
                object_id=form_object_id,
                body=form_comment,
                parent=parent,
            )
            if self.request.is_ajax():
                comments = Comment.objects.filter(content_type=content_type, object_id=form_object_id)
                instance = content_type.model_class().objects.get(id=form_object_id)
                new_form = make_new_form(self.request, form_object_id, content_type)
                context = {
                    "form": new_form,
                    "comments": comments,
                    "instance": instance,
                }
                html = render_to_string("comments_partial.html", context=context, request=self.request)
                serialized_data = json.dumps({"html": html})
                return HttpResponse(serialized_data, content_type="application/json")
            return HttpResponseRedirect(comment.get_absolute_url())

    def get_context_data(self, object_pk=None, content_type=None, **kwargs):
        super(CommentReplyView, self).get_context_data(**kwargs)
        form = make_new_form(self.request, object_pk, content_type)
        context = {
            "comment": self.parent,
            "form": form,
        }
        return context


class CommentDeleteView(TemplateView):
    template_name = "comments.html"
    partial_template = "comments_partial.html"

    def get(self, *args, **kwargs):
        comment = int(kwargs.get("comment"))
        comment_instance = get_object_or_404(Comment, id=comment)
        if comment_instance.user != self.request.user:
            response = HttpResponse("<h1>You are not allowed to perform this action</h1>")
            response.status_code = 403
            return response
        obj_id = comment_instance.object_id
        c_type = comment_instance.content_type
        comment_instance.delete()
        context = self.get_context_data(object_pk=obj_id, content_type=c_type, **kwargs)
        context["comments"] = Comment.objects.filter(object_id=obj_id, content_type=c_type)
        context["instance"] = c_type.model_class().objects.get(id=obj_id)
        if self.request.is_ajax():
            html = render_to_string("comments_partial.html", context=context, request=self.request)
            serialized_data = json.dumps({"html": html})
            return HttpResponse(serialized_data, content_type="application/json")
        return render(self.request, template_name="comments.html", context=context)

    def get_context_data(self, object_pk=None, content_type=None, **kwargs):
        super(CommentDeleteView, self).get_context_data(**kwargs)
        form = make_new_form(self.request, object_pk, content_type)
        context = {
            "form": form,
        }
        return context
