from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, \
    PasswordResetView
from django.shortcuts import render, redirect
from django.utils.timezone import utc
from django.views.generic import CreateView, DetailView
from django_ratelimit.decorators import ratelimit
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
#from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.generic import UpdateView
from django.contrib.auth.forms import PasswordChangeForm


class ResetPasswordView(PasswordResetView):
    template_name = 'main/change_password.html'


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'main/change_password_done.html'


def send_message_on_email(request):
    # message = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
    send_mail('Subject here', 'Here is the message', 'nikita.hom1977@gmail.com', ['warwarkot@gmail.com', 'ladnoxd4@gmail.com'], fail_silently=False)


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'main/change_password.html'
    success_url = reverse_lazy('main_page')


class ChangeFormView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'main/change_password.html'
    success_url = reverse_lazy('/')


def change_password(request, pk):
    user = CustomUser.objects.get(id=pk)
    form = PasswordChangeForm(request.POST, request.FILES)
    if form.is_valid():
        usr = form.save(commit=False)
        #user.password = usr.password
        #user.save()
        user.set_password(usr.password)
        user.save()
        return redirect('/')
    else:
        return redirect('comment_page')
    #return render(request, 'main/change_password.html', {'form': form})

# class ChangePassword(PasswordChangeView):
#     form_class = CustomUserCreationForm
#     success_url = '/'
#     template_name = 'main/change_password.html'
#
#
# class ChangePasswordDone(PasswordChangeDoneView):
#     template_name = 'main/login.html'


def get_queryset(self):
    species_id = self.kwargs['species_id']
    return self.model.objects.filter(species_id=species_id)


# def user_change_password(request, pk):
#     user = CustomUser.objects.get(id=pk)
#     form = PasswordForm()
#     if request.method == 'POST':
#         form = PasswordForm(request.POST, request.FILES)
#         if form:
#             usr = form.save(commit=False)
#             user.password = usr.password
#             user.save()
#             user.set_password(usr)
#             user.save()
#             return redirect('/')
#         else:
#             messages.error(request, 'Ошибка')
#     return render(request, 'main/change_password.html', {'form': form})


@login_required
def delete_own_comment(request, question_id):
    #comment = get_object_or_404(Question, pk=question_id)
    comment = Question.objects.get(id=question_id)
    if Question.author == request.user:
        comment.is_removed = True
        comment.save()
    return redirect('comment_page')


class CreateComment(CreateView):
    form_class = QuestionForm
    success_url = '/'
    template_name = 'main/create_comment.html'


@ratelimit(key='ip', rate='2/m')
def create_comment(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            # question.answer_by = id #request.user
            question.save()
            return redirect('comment_page')
    else:
        form = QuestionForm()
    return render(request, 'main/create_comment.html', {'form': form})


def main_page(request):
    #cont = CustomUser.objects.all()
    #con = cont[id]
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            #user = form.get.objects.latests.filter(id=request.user.id)
            login(request, user)
            return redirect('main_page')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = UserLoginForm()
    return render(request, 'main/main_page.html', {'form': form})


def comment(request):
    model = Question.objects.all().order_by('-created_add')
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            #user = form.get.objects.latests.filter(id=request.user.id)
            login(request, user)
            return redirect('main_page')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = UserLoginForm()

    if request.method == 'POST':
        form2 = QuestionForm(request.POST, request.FILES)
        if form2.is_valid():
            question = form2.save(commit=False)
            question.author = request.user
            # question.answer_by = id #request.user
            question.save()
            return redirect('comment_page')
    else:
        form2 = QuestionForm()
    return render(request, 'main/comment_page.html', {'question': model, 'form': form, 'form2': form2})


def delite(request, pk):
    comment = Question.objects.get(id=pk)
    comment.delete()
    comments = Question.objects.filter(answer_by=pk)
    comments.delete()
    return redirect('comment_page')


class Register(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/'
    template_name = 'main/create_user.html'


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.avatar:
                user.avatar = 'photos/user.png'
            return redirect('/')
        else:
            pass
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/create_user.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('main_page')


def user_login(request):
    if request.method == 'POST':
        #form = CustomUserChangeForm(data=request.POST)
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
        else:
            messages.error(request, 'Ошибка')
    else:
        #form = CustomUserChangeForm()
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})


def user_profile(request):
    model = Question.objects.filter(answer_by_id=request.user.id)
    return render(request, 'main/user_profile.html', {'model': model})


@ratelimit(key='ip', rate='2/m')
def answer(request, pk): #answer_by_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.answer_by = pk #answer_by_id
            question.save()
            return redirect('comment_page')
    else:
        form = QuestionForm()
    return render(request, 'main/create_comment.html', {'form': form})


# def edit_profile(request):
#     if request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, request.FILES)
#         if form.is_valid():
#             cstusr = form.save(commit=False)
#
#     else:
#         form = CustomUserChangeForm()
#     return render(request, 'main/edit_profile.html', {'form': form})


class EditProfile(CreateView):
    form_class = CustomUserChangeForm
    template_name = 'main/edit_profile.html'
    context_object_name = 'form'
    success_url = '/'


class Comments(DetailView):
    model = Question
    template_name = 'main/comments.html'
    context_object_name = 'comment'


def commments(request, pk):
    model = Question.objects.filter(answer_by=pk)
    creator = Question.objects.filter(id=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.answer_by = pk #answer_by_id
            question.save()
            return redirect('comment_page')
    else:
        form = QuestionForm()
    return render(request, 'main/comments.html', {'model': model, 'creator': creator, 'form2': form})


#@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = CustomChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('/')
        else:
            print(user_form.errors)
    else:
        user_form = CustomChangeForm()
    return render(request, 'main/edit_profile.html', {'form': user_form})


#@ratelimit(key='ip', rate='2/5m')
@login_required
def update_user(request, pk):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES)
        Userr = CustomUser.objects.get(id=pk)
        if form.is_valid():
            #img = form.cleaned_data['avatar']
            changed_user = form.save(commit=False)
            #changed_user.user = request.user
            if changed_user.username:
                Userr.username = changed_user.username
            if changed_user.description:
                Userr.description = changed_user.description
            if changed_user.avatar:
                Userr.avatar = changed_user.avatar
            if changed_user.information:
                Userr.information = changed_user.information
            changed_user.save()
            Userr.save()
            cont = CustomUser.objects.latest('id').id
            usr = CustomUser.objects.get(id=cont)
            usr.delete()
            #userr = CustomUser.objects.filter(id=pk)[:4].values_list("id", flat=True)
            #CustomUser.objects.exclude(pk__in=list(userr)).delete()
            #userr.delete()

            return redirect('/')
    else:
        form = CustomUserChangeForm()
    return render(request, 'main/edit_profile.html', {'form': form})


def profile(request, author_id):
    model = CustomUser.objects.filter(id=author_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES)
        Userr = CustomUser.objects.get(id=author_id)
        if form.is_valid():
            #img = form.cleaned_data['avatar']

            changed_user = form.save(commit=False)
            Userr.username = changed_user.username

            Userr.description = changed_user.description

            Userr.avatar = changed_user.avatar
            changed_user.save()
            Userr.save()
            cont = CustomUser.objects.latest('id').id
            usr = CustomUser.objects.get(id=cont)
            usr.delete()
            #return render(request, 'main/profile.html', {'model': model, 'form': form})
            return redirect('/')
    else:
        form = CustomUserChangeForm()
    return render(request, 'main/profile.html', {'model': model, 'form': form})


# def change_password(request, pk):
#     user = CustomUser.objects.get(id=pk)
#     if request.method == 'POST':
#         form = CustomUserChangePassword(request.POST, request.FILES)
#         if form.is_valid():
#             changed_user = form.save(commit=False)
#             user.password1 = changed_user.password1
#             #changed_user.delete()
#             user.save()
#             return redirect('/')
#         else:
#             return redirect('comment_page')
#     else:
#         form = CustomUserChangePassword()
#     return render(request, 'main/change_password.html', {'form': form})


#@decorator_request_user_is_aunteficated():
def password_change_done(request):
    logout(request)
    return redirect('/')
