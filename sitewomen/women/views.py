from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate

from .forms import UploadFileForm, WomenForm, CommentForm
from .models import Women, UploadFiles, Comment


menu = [
        {'title': "Про сайт", 'url_name': 'about'},
        {'title': "Зворотній звязок", 'url_name': 'contact'},
]

superuser_menu = [
        {'title': "Додати зображення", 'url_name': 'addpicture'},
        {'title': "Зворотній звязок", 'url_name': 'contact'},
        {'title': 'Додати статтю', 'url_name': 'addpage'}
]

# categories_db = [
#     {'id': 1, 'name': 'Актриси'},
#     {'id': 2, 'name': 'Співачки'},
#     {'id': 3, 'name': 'Спортсменки'},
# ]


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


def about(request):
    data = {'menu': menu, 'user': request.user}
    return render(request, 'women/about.html', data)


def addpage(request):
    if request.method == 'POST':
        form = WomenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправлення на головну сторінку після успішного додавання
    else:
        form = WomenForm()

    data = {'title': 'Додати статтю', 'form': form, 'menu': menu, 'superuser_menu': superuser_menu}
    return render(request, 'addpage.html', data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')


def contact(request):
    data = {'menu': menu, 'superuser_menu': superuser_menu}
    return render(request, 'women/contact.html', data)


def add_picture(request):  # зберігає в БД
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


@login_required  # Додаємо декоратор для перевірки, чи користувач увійшов в систему
def post_detail(request, post_id):
    post = get_object_or_404(Women, id=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Вказуємо автора коментаря
            new_comment.save()
            form = CommentForm()  # Очищення форми для подальших коментарів
    else:
        form = CommentForm()

    return render(request, 'women/post_detail.html', {'post': post,
                                                      'comments': comments,
                                                      'form': form,
                                                      'menu': menu,
                                                      'superuser_menu': superuser_menu})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Перевірка, чи користувач, який намагається видалити коментар, є автором коментаря
    if request.user == comment.author:
        comment.delete()
        return JsonResponse({'message': 'Коментар видалено успішно.'})
    else:
        return HttpResponseForbidden('Ви не маєте дозволу на видалення цього коментаря.')
