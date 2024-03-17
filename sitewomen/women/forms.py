from django import forms
from women.models import Women, Comment


class UploadFileForm(forms.Form):
    file = forms.FileField(label='File')


class WomenForm(forms.ModelForm):
    class Meta:
        model = Women
        # fields = ['title', 'content', 'cat', 'photo']
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Автора більше не потрібно вказувати, оскільки він прив'язаний до користувача

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'rows': 3, 'cols': 50})  # Налаштування атрибутів текстового поля
