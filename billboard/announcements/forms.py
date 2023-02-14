from django import forms
from django.core.exceptions import ValidationError
from .models import Announcement, Comment


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'category',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 3:
            raise ValidationError({
                "title": "Title must be at least 3 characters!"
            })
        text = cleaned_data.get("text")
        if text == title:
            raise ValidationError({
                "text": "The text must not match the title!"
            })
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
