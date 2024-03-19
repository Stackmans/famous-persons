from django.urls import path, re_path, register_converter
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('addpage/', views.NewPage.as_view(), name='addpage'),
    path('addpicture/', views.add_picture, name='addpicture'),
    path('post/<int:post_id>/', views.post_detail, name='post'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('category/<int:cat_id>/', views.WomenCategories.as_view(), name='category'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('login/', views.LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
