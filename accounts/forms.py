from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import VolunteerProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=17, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    profile_image = forms.ImageField(required=False)
    role = forms.ChoiceField(choices=get_user_model().ROLE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 
                  'phone_number', 'address', 'profile_image', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.role = self.cleaned_data['role']
        
        if commit:
            user.save()
            # Create volunteer profile if user is a volunteer
            if user.role == 'volunteer':
                VolunteerProfile.objects.create(user=user)
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_image')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = VolunteerProfile
        fields = ('bio', 'achievements', 'participated_campaigns')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'achievements': forms.Textarea(attrs={'rows': 4}),
            'participated_campaigns': forms.Textarea(attrs={'rows': 4}),
        }