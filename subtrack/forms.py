from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Subscription, SubscriptionUsage


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = (
            'service_name',
            'category',
            'amount',
            'billing_cycle',
            'billing_date',
            'trial_end_date',
            'reminder_days_before',
            'status',
            'is_active',
            'notes',
        )
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'trial_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UsageForm(forms.ModelForm):
    class Meta:
        model = SubscriptionUsage
        fields = ('month', 'used', 'note')
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
        }
