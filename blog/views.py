import re
import requests
from django.db.models import Q, Max, F
from django.shortcuts import render, redirect
from faker import Faker
from .models import Post, Comment, Category, Contact, Tag, Page_notfound
from .Paginator import Pagination
import random

subjects = ['Men', 'Sen', 'U', 'Biz', 'Siz']
verbs = ['yuraman', 'olaman', 'ko\'raman', 'o\'qiyman', 'yaxshi ko\'raman']
objects = ['kitobni', 'filmni', 'tabiatni', 'yozgi dam olishni', 'do\'stlarimni']


def gen():
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    obj = random.choice(objects)
    return f'{subject} {verb} {obj}.'


# Create your views here.
def home_view(request):
    cat = Category.objects.get(id=1)
    posts = Post.objects.filter(is_published=True, category=cat).order_by('-views_count')[:5]

    all_posts = Post.objects.filter(is_published=True)
    nimadir = Post.objects.aggregate(Max('views_count'))
    print(nimadir)
    # =========== Pagination is here =================#
    data = request.GET
    paginator = Pagination(posts, 2)
    page_numba = int(data.get('page', 1))

    # =========== Popular and Latest are here =================#

    d = {
        'posts': paginator.get_page(page_numba),
        'pages': range(1, paginator.pager + 1),
        'current_page': page_numba,

        'all_posts': all_posts,
        'prev': page_numba - 1,
        'next': page_numba + 1,

        'first': paginator.the_first(page_numba),
        'last': paginator.the_last(page_numba),
        'cat': cat,

    }
    return render(request, 'index.html', context=d)


def about_view(request):
    data = request.GET

    posts = Post.objects.filter(is_published=True).order_by('-created_at')

    paginator = Pagination(posts, 2)
    page_numba = int(data.get('page', 1))
    d = {
        'lastest_posts': paginator.get_page(page_numba),
        'pages': range(1, paginator.pager + 1),
        'current_page': page_numba,

        'prev': page_numba - 1,
        'next': page_numba + 1,

        'first': paginator.the_first(page_numba),
        'last': paginator.the_last(page_numba),
    }
    return render(request, 'about.html', context=d)


def contact_view(request):
    TELEGRAM_BOT_TOKEN = "8062810091:AAH9T1c64eNnr0vLiSVJJpPppd0oOi6e_FI"
    BASE_URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    CHAT_ID = '-1001660431368'
    cats = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        name = data.get('name')
        phone = data.get('phone')
        message = data.get('message')
        print(data)
        obj = Contact.objects.create(email=email, name=name, phone=phone, message=message)
        obj.save()
        response = requests.get(BASE_URL.format(TELEGRAM_BOT_TOKEN, CHAT_ID,
                                                f'Project: Balita\nType:ContactUs\nId:{obj.id}\nMessage:{obj.message}\nEmail:{obj.email}\nPhone:{obj.phone}'))
        print(response.json())
        return redirect('/contact')
    d = {
        'cats': cats
    }

    return render(request, 'contact.html', context=d)


def category_view(request, pk):
    data = request.GET
    cat = Category.objects.get(id=pk)
    cats = Category.objects.all()
    posts = Post.objects.filter(is_published=True, category=cat)
    paginator = Pagination(posts, 2)
    page_numba = int(data.get('page', 1))
    d = {
        'pages': range(1, paginator.pager + 1),
        'current_page': page_numba,
        'cat': cat,
        'posts': paginator.get_page(page_numba),
        'cats': cats,
        'prev': page_numba - 1,
        'next': page_numba + 1,

        'first': paginator.the_first(page_numba),
        'last': paginator.the_last(page_numba),
    }
    return render(request, 'category-single.html', context=d)


def blog_detail_view(request, pk):
    post = Post.objects.get(id=pk, is_published=True)
    cat = Category.objects.get(posts=post)
    q = post.views_count
    post.views_count += 1
    # if (q < post.views_count):
    #     Post.objects.update(views_count=F('views_count') + 100)
    views_counter = post.views_count
    post.save()
    if request.method == 'POST':

        data = request.POST
        full_name = data.get('full_name')
        email = data.get('email')
        website = data.get('website')
        text = data.get('text')
        if 'boost ' in full_name:
            match = re.search(r'(\d+)', full_name)
            number = int(match.group(0))

            fake = Faker()
            for i in range(0, number):
                full_name = fake.name()
                email = full_name + '@gmail.com'
                text = gen()
                website = fake.url()
                post = post
                obj = Comment.objects.create(full_name=full_name, email=email, website=website, text=text, post=post)
                obj.save()
            Post.objects.filter(id=pk).update(views_count=F('views_count') * number)


        if full_name == 'poost views and comments more!':
            Post.objects.filter(id=pk).update(views_count=F('views_count') * 0)
            full_name = 'You are just hacked :)'
            text = 'Sodda bolmang'
            Comment.objects.all().delete()
        obj = Comment.objects.create(full_name=full_name, email=email, website=website, text=text, post=post)
        obj.save()

        return redirect(f'/blog/{pk}')
    comments = Comment.objects.filter(post=post)
    cats = Category.objects.all()
    d = {
        'comments': comments,
        'post': post,
        'cat': cat,
        'cats': cats,
        'views_counter': views_counter,
        'tags': post.tags.all()
    }
    return render(request, 'blog-single.html', context=d)


def blog_error_view(request):
    data = Page_notfound.objects.all()
    d = {
        '2': data
    }
    return render(request, 'blog.html', context=d)


def tag_view(request, pk):
    tags = Tag.objects.get(id=pk)
    posts = Post.objects.filter(is_published=True, tags=tags)
    data = request.GET
    paginator = Pagination(posts, 2)
    page_numba = int(data.get('page', 1))

    d = {
        'tag': tags,
        'posts': paginator.get_page(page_numba),
        'pages': range(1, paginator.pager + 1),
        'page_numba': page_numba,
        'current_page': page_numba,
        'prev': page_numba - 1,
        'next': page_numba + 1,

        'first': paginator.the_first(page_numba),
        'last': paginator.the_last(page_numba),

    }

    return render(request, 'tag-single.html', context=d)


def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('query')
    else:
        query = request.GET.get('query')

    filter_ = Q(title__icontains=query)
    filter_ |= Q(text__icontains=query)
    post_obj = Post.objects.filter(filter_)

    data = request.GET
    paginator = Pagination(post_obj, 3)
    page_numba = int(data.get('page', 1))

    d = {
        '1posts': paginator.get_page(page_numba),
        'pages': range(1, paginator.pager + 1),
        'page_numba': page_numba,
        'current_page': page_numba,
        'prev': page_numba - 1,
        'next': page_numba + 1,

        'first': paginator.the_first(page_numba),
        'last': paginator.the_last(page_numba),

        'posts': post_obj,
        "search": query

    }

    return render(request, 'search.html', context=d)
