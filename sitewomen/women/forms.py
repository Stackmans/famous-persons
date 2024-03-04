from django import forms
from women.models import Women, Comment


class UploadFileForm(forms.Form):
    file = forms.FileField(label='File')


class WomenForm(forms.ModelForm):
    class Meta:
        model = Women
        fields = ['title', 'content', 'cat', 'photo']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
