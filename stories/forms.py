from django import forms
from .models import Story, Category
from accounts.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'description', 'category', 'required_amount', 'images', 'supporting_documents')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Ensure the category queryset is available
            self.fields['category'].queryset = Category.objects.all()


class StoryApprovalForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }