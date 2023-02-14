from django.contrib import admin
from .models import Author, Category, Announcement, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Announcement)
admin.site.register(Comment)
