from django import forms
from .models import Donation
from stories.models import Story


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('amount', 'payment_screenshot')
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1', 'step': '0.01', 'class': 'form-control'}),
            'payment_screenshot': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.story = kwargs.pop('story', None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if self.story:
            remaining_amount = self.story.required_amount - self.story.collected_amount
            if amount > remaining_amount:
                raise forms.ValidationError(f"Amount exceeds remaining required amount. Only {remaining_amount} left to reach the goal.")
        return amount