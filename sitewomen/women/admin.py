from django.contrib import admin
from .models import *


class WomenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Women, WomenAdmin)