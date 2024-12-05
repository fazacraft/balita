from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=30)
    website = models.URLField()
    text = models.TextField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.full_name} - {self.created_at}'


class Tag(models.Model):
    name = models.CharField(max_length=25)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=30)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    text = models.TextField()
    image = models.ImageField(upload_to='media/')
    image2 = models.ImageField(upload_to='media/')
    image3 = models.ImageField(upload_to='media/')
    description = RichTextField(blank=True, null=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def comments_count(self):
        return self.comments.count()


class Category(models.Model):
    name = models.CharField(max_length=30)

    def post_counter(self):
        return self.posts.count()

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    message = models.TextField()

    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Page_notfound(models.Model):
    image= models.ImageField(upload_to='qatgadir/')