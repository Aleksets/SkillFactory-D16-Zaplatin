from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Model Author
# Model, that contains objects of all Authors.
# It contains "one to one" field "author" related to integrated model "User".
class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username


# Model Category
# Categories of announcements
# It contains 1 field: category_name (unique)
class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category_name


# Model Announcement
# Announcements, that Authors create.
# Every announcement can have one or more Categories.
# It contains:
# "one to many" field "author" related to model "Author"
# field "add_date", that automatically collect date and time of creation
# "many to many" field "category" related to model "Category"
# field "title"
# field "text"
class Announcement(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='author')
    add_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name='categories', verbose_name='category')
    title = models.CharField(max_length=255, verbose_name='title')
    text = RichTextUploadingField(config_name='default')

    def preview(self):
        if len(self.text) > 51:
            return f"{self.text[:51]}..."
        elif len(self.text) == 51:
            return self.text[:51]
        else:
            return self.text

    def get_absolute_url(self):
        return reverse('announcement', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}\n{self.add_date.strftime("%d.%m.%Y")}\n{self.text}'


# Model Comment
# You can post your commentaries under announcements
# It contains:
# "one to many" field "announcement" related to model "Announcement"
# "one to many" field "author" related to integrated model "User"
# field "text"
# field "add_date", that automatically collect date and time of creation
# field "is_new"
class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='text')
    add_date = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.author}\n{self.add_date.strftime("%d.%m.%Y")}\n{self.text}'
