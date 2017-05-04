from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostCreateForm


# Create your views here.
def home(request):
    queryset_list = Post.objects.all()
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


def create(request):
    form = PostCreateForm(files=request.FILES or None)
    context = {
        "form": form
    }

    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Succesfully created %s" % instance.title)
            return redirect(instance.get_absolute_url())
        else:
            messages.error(request, "Could not create post.")
            return render(request, "create.html", context)

    return render(request, "create.html", context)


def detail(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    context = {
        "post": instance
    }
    return render(request, "detail.html", context)


def update(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    form = PostCreateForm(request.FILES, instance=instance)
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


def delete(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    title = instance.title
    instance.delete()
    messages.success(request, "Succesfully deleted %s" % title)
    return redirect(reverse("posts:home"))


