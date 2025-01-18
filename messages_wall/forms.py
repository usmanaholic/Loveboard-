from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Message, MessageWall, Timeline, SpecialDate

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class MessageForm(forms.ModelForm):
    media_files = MultipleFileField(
        required=False,
        help_text='You can select multiple files at once.'
    )
    
    class Meta:
        model = Message
        fields = ['content', 'theme', 'is_public', 'is_anonymous', 'background_color', 'font_style']
        widgets = {
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'content': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_media_files(self):
        files = self.files.getlist('media_files')
        for file in files:
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Each file must be less than 5MB')
        return files

class MessageWallForm(forms.ModelForm):
    class Meta:
        model = MessageWall
        fields = ['title', 'theme', 'is_public']

class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = ['title', 'description', 'date', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SpecialDateForm(forms.ModelForm):
    class Meta:
        model = SpecialDate
        fields = ['title', 'date', 'reminder']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }