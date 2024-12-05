from django.contrib import admin
from .models import Category, Comment, Post, Contact, Tag, Page_notfound

# Register your models here.


admin.site.register(Category)
admin.site.register(Comment)

admin.site.register(Page_notfound)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'created_at', 'category', 'views_count')
    list_display_links = ('title', 'category')
    list_filter = ('category', 'is_published', 'created_at')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'is_solved')
    list_display_links = ('name','id')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
