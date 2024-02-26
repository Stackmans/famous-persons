from django import forms
from women.models import Women


class UploadFileForm(forms.Form):
    file = forms.FileField(label='File')


class WomenForm(forms.ModelForm):
    class Meta:
        model = Women
        fields = ['title', 'content', 'photo']
