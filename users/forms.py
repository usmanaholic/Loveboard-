# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import UserProfile
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        help_text='Your birth date is required for age verification.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Username can only contain letters, numbers, and underscores.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                birth_date=self.cleaned_data['birth_date']
            )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'avatar',
            'bio',
            'location',
            'website',
            'display_email',
            'theme_preference',
            'notification_preferences',
            'privacy_settings'
        )
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'privacy_settings': forms.CheckboxSelectMultiple(),
            'notification_preferences': forms.CheckboxSelectMultiple(),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image file size must be less than 5MB.')
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = avatar.name.lower().split('.')[-1]
            if f'.{ext}' not in valid_extensions:
                raise ValidationError('Please upload a valid image file (jpg, jpeg, png, gif).')
        return avatar

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('notification_preferences',)
        widgets = {
            'notification_preferences': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notification_preferences'].choices = [
            ('email_messages', 'Email notifications for new messages'),
            ('email_wall_activity', 'Email notifications for wall activity'),
            ('email_special_dates', 'Email reminders for special dates'),
            ('browser_notifications', 'Browser notifications'),
            ('mobile_notifications', 'Mobile notifications')
        ]

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('privacy_settings',)
        widgets = {
            'privacy_settings': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['privacy_settings'].choices = [
            ('show_email', 'Show email to other users'),
            ('show_full_name', 'Show full name to other users'),
            ('show_location', 'Show location to other users'),
            ('allow_messages', 'Allow messages from non-friends'),
            ('public_profile', 'Make profile public'),
            ('show_online_status', 'Show online status')
        ]

class AccountDeletionForm(forms.Form):
    confirmation = forms.BooleanField(
        required=True,
        label='I understand that this action cannot be undone and all my data will be permanently deleted.'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label='Enter your password to confirm deletion'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise ValidationError('Incorrect password. Please try again.')
        return password