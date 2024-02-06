from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView
from .models import Women
from django.contrib.auth import login, authenticate

menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "Зворотній звязок", 'url_name': 'contact'},
        ]

categories_db = [
    {'id': 1, 'name': 'Актриси'},
    {'id': 2, 'name': 'Співачки'},
    {'id': 3, 'name': 'Спортсменки'},
]


def index(request):
    data = {'title': 'головна сторінка',
            'menu': menu,
            'posts': Women.objects.all(),
            'cat_selected': 0,
            }
    return render(request, 'women/index.html', data)


def show_category(request, cat_id):
    data = {'title': 'Відображення по рубрикам',
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
    }
    return render(request, 'women/biography.html', data)


def about(request):
    data = {'title': 'Про сайт', 'menu': menu}
    return render(request, 'women/about.html', data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')


def contact(request):
    return HttpResponse('Зворотній звязок')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Аутентифікація користувача
            user = authenticate(request, username=user.username, password=request.POST['password1'])

            # Увійти в систему користувача
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
