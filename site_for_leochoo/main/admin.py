from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'answer_by', 'created_add', 'author', ]
    list_display_links = ['id', 'text', 'answer_by', 'author', 'created_add', ]


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'username', 'description', 'email', 'avatar', 'password']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Question, QuestionAdmin)
