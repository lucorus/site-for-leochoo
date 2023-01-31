from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', main_page, name='main_page'),
    path('register/', Register.as_view(), name='Register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user_logout/', user_logout, name='user_logout'),
    path('create_comment', create_comment, name='create_comment'),
    path('comment_page', comment, name='comment_page'),
    #path('user_profile', user_profile, name='user_profile'),
    path('profile/<int:author_id>', profile, name='profile'),
    path('answer/<int:pk>', answer, name='answer'),
    path('comments/<int:pk>', commments, name='comments'),
    path('delete/<int:question_id>', delete_own_comment, name='delete'),
    path('edit_profile/<int:pk>', update_user, name='edit_profile'),
    path('delite/<int:pk>', delite, name='delite'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name='main/change_password.html')),
    path('password/', ChangePasswordView.as_view(template_name='change/change_password.html')),
    path('send_message', send_message_on_email, name='send_message'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset/done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    #path('password_reset/', PasswordResetDoneView.as_view(), name='password_reset_done')
    #path('password/<int:pk>', ChangeFormView.as_view(), name='change_password'),
    # path('password_change/', ChangePassword.as_view(), name='change_password'),
    # path('password_change/done/', ChangePasswordDone.as_view(), name='password_change_done'),
]
