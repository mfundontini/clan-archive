from urllib import quote_plus

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostCreateForm
from archive.comments.models import Comment
from archive.comments.forms import CreateCommentForm


# Create your views here.
def home(request):
    queryset_list = Post.objects.active()
    if request.user.is_staff:
        queryset_list = Post.objects.all()
    search = request.GET.get("q")
    if search:
        queryset_list = queryset_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search) |
            Q(author__username__icontains=search)
        ).distinct()
    paginator = Paginator(queryset_list, 10)  # Show 10 posts per page
    page_index = "page"
    page = request.GET.get(page_index)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "posts": queryset,
        "page": page_index
    }
    return render(request, "home.html", context)


@login_required()
def create(request):
    if not request.user.is_staff:
        raise Http404
    form = PostCreateForm(files=request.FILES or None)
    context = {
        "form": form
    }

    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, "Succesfully created %s" % instance.title)
            return redirect(instance.get_absolute_url())
        else:
            messages.error(request, "Could not create post.")
            return render(request, "create.html", context)

    return render(request, "create.html", context)


def detail(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    content = instance.title
    content = quote_plus(content)
    comments = Comment.objects.filter_by_instance(instance)
    form = None

    if request.user.is_authenticated():
        initial = {
            "content_type": instance.content_type,
            "object_id": instance.id,
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
        "post": instance,
        "url_string": content,
        "comments": comments,
        "form": form,
    }
    return render(request, "detail.html", context)


@login_required()
def update(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    form = PostCreateForm(instance=instance)
    context = {
        "form": form
    }
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES, instance=instance)
        context["form"] = form

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Succesfully updated %s" % instance.title)
            return redirect(instance.get_absolute_url())
        else:
            form = PostCreateForm(instance=instance)
            context["form"] = form
            messages.error(request, "Could not update %s" % instance.title)
            return render(request, "create.html", context)

    return render(request, "update.html", context)


@login_required()
def delete(request, pk):
    if not request.user.is_staff:
        raise Http404
    instance = get_object_or_404(Post, pk=pk)
    title = instance.title
    instance.delete()
    messages.success(request, "Successfully deleted %s" % title)
    return redirect(reverse("posts:home"))
