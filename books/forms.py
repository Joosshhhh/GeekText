from django import forms
from .models import Comment, Rating


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)


