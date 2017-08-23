from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("Username or Password Incorrect.")

            if user and not user.is_active:
                raise forms.ValidationError("This user has been blocked.")
        return super(LoginForm, self).clean()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(label="Email Address")
    confirm_email = forms.CharField(label="Confirm Email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("This email already exists.")
        return email

    def clean_confirm_email(self):
        email = self.cleaned_data.get("email")
        confirm_email = self.cleaned_data.get("confirm_email")

        if email and confirm_email:
            if email != confirm_email:
                raise forms.ValidationError("Make sure the emails match.")
        return confirm_email

    class Meta:
        model = User
        fields = ["username", "password", "email", "confirm_email"]
