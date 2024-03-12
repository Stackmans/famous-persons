from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')  # зберігає в папці uploads_model


class Women(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField(blank=True, max_length=500)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT)
    photo = models.OneToOneField(UploadFiles, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Photo')

    # file = models.FileField(upload_to='uploads_model')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Women, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Поле для зв'язку з моделлю User
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.created_at}'
