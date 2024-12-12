from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile,PassoutYear, PlacementDetails
from django.contrib.auth.forms import PasswordChangeForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.userprofile.phone_number = self.cleaned_data['phone_number']
            user.userprofile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['email'].initial = self.instance.email
            self.fields['username'].initial = self.instance.username

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number']

class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter your new password.",
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter the same password as above, for verification.",
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user
    
class PassoutYearForm(forms.ModelForm):
    class Meta:
        model = PassoutYear
        fields = ['year']
class PlacementDetailsForm(forms.ModelForm):
    class Meta:
        model = PlacementDetails
        fields = ['name', 'usn', 'company_name', 'ctc']