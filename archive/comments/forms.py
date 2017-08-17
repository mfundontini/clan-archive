from django import forms


class CreateCommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    comment_body = forms.CharField(label="", widget=forms.Textarea, max_length=200)
