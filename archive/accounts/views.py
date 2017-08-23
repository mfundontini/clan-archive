from django.views.generic import FormView
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import LoginForm, RegisterForm


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def form_valid(self, form):
        next_view = self.request.GET.get("next")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        if next_view:
            return HttpResponseRedirect(next_view)
        return HttpResponseRedirect(reverse("posts:home"))


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "register.html"

    def form_valid(self, form):
        new_user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        new_user.set_password(password)
        new_user.save()
        user = authenticate(username=new_user.username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse("posts:home"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("accounts:login"))
