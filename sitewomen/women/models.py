from django.db import models


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Women(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField(blank=True, max_length=500)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/',default=None, blank=True, null=True, verbose_name='Photo')
    photo = models.OneToOneField(UploadFiles, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Photo')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name
