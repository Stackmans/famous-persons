from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate

from .forms import UploadFileForm, WomenForm
from .models import Women, UploadFiles

menu = [
        {'title': "Про сайт", 'url_name': 'about'},
        {'title': "Зворотній звязок", 'url_name': 'contact'},
]

superuser_menu = [
        {'title': "Додати зображення", 'url_name': 'addpicture'},
        {'title': "Зворотній звязок", 'url_name': 'contact'},
        {'title': 'Додати статтю', 'url_name': 'addpage'}
]

categories_db = [
    {'id': 1, 'name': 'Актриси'},
    {'id': 2, 'name': 'Співачки'},
    {'id': 3, 'name': 'Спортсменки'},
]


def index(request):
    data = {'title': 'головна сторінка',
            'menu': menu,
            'superuser_menu': superuser_menu,
            'posts': Women.objects.all(),
            'cat_selected': 0,
            }
    return render(request, 'women/index.html', data)


def show_category(request, cat_id):
    data = {'title': 'Відображення по рубрикам',
            'superuser_menu': superuser_menu,
            'menu': menu,
            'posts': Women.objects.all(),
            'cat_selected': cat_id,
            }
    return render(request, 'women/list_women_in_category.html', data)


def show_post(request, post_id):
    # Отримуємо об'єкт з бази даних за заданим post_id
    try:
        post = Women.objects.get(id=post_id)
    except Women.DoesNotExist:
        # Обробляємо випадок, коли об'єкт не знайдений
        post = None

    data = {
        'post': post,
        'menu': menu,
        'superuser_menu': superuser_menu
    }
    return render(request, 'women/biography.html', data)


def about(request):
    data = {'menu': menu, 'user': request.user}
    return render(request, 'women/about.html', data)


# def addpage(request):
#     data = {'menu': menu, 'superuser_menu': superuser_menu, 'user': request.user}
#     return render(request, 'women/addpage.html', data)


def addpage(request):
    if request.method == 'POST':
        form = WomenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправлення на головну сторінку після успішного додавання
    else:
        form = WomenForm()

    data = {'title': 'Додати людину', 'form': form, 'menu': menu, 'superuser_menu': superuser_menu}
    return render(request, 'addpage.html', data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')


def contact(request):
    data = {'menu': menu, 'superuser_menu': superuser_menu}
    return render(request, 'women/contact.html', data)


def add_picture(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    data = {'superuser_menu': superuser_menu, 'form': form, 'user': request.user}
    return render(request, 'women/addpicture.html', data)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user:
                login(request, user)

            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'women/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Аутентифікація користувача
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            # Увійти в систему користувача
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'women/login.html', {'form': form})

# biography.html

# {% extends 'base.html' %}
# {% block content %}
#   {% if post %}
#     <h2>{{ post.title }}</h2>
#     <p>{{ post.content }}</p>
#     {% if post.is_published %}
#       <p>This post is published.</p>
#     {% else %}
#       <p>This post is not published.</p>
#     {% endif %}
#   {% else %}
#     <p>Post not found.</p>
#   {% endif %}
# {% endblock %}
