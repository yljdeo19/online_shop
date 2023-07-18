from django.contrib import admin
from .models import Category, Good, Comment, BackCall

admin.site.register(Category)
admin.site.register(Good)
admin.site.register(Comment)
admin.site.register(BackCall)

