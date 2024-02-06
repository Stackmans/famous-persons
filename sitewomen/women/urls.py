from django.urls import path, re_path, register_converter
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000
    path('about/', views.about, name='about'),  # http://127.0.0.1:8000/about/
    path('contact/', views.contact, name='contact'),
    path('post/<int:post_id>/', views.show_post, name='post'),  # http://127.0.0.1:8000/post/1/
    path('category/<int:cat_id>/', views.show_category, name='category'),  # http://127.0.0.1:8000/category/1/

    path('register/', views.register, name='register'),
    # path('login/', AuthLoginView.as_view(), name='login'),
    # path('login/', LoginView.as_view(), name='login'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
