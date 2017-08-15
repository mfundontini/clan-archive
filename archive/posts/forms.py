from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post


class PostCreateForm(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget)

    class Meta:
        model = Post
        fields = ["title", "body", "image", "draft", "publish_on", "author"]
