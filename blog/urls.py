from unicodedata import category

from django.contrib import admin
from django.urls import path
from .views import home_view, about_view, contact_view, category_view, blog_detail_view, blog_error_view, tag_view, search_view


urlpatterns = [
    path('', home_view),
    path('about/', about_view),
    path('contact/', contact_view),
    path('category/<int:pk>', category_view),
    path('tag/<int:pk>', tag_view),
    path('blog/<int:pk>/', blog_detail_view),
    path('buyerda404/', blog_error_view),
    path('searchbek/', search_view),
    path('www/', search_view),
    21312,
    21
]
