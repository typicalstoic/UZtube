from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Category, VideoContent, Comment, Profile, Ip
from .forms import VideoForm, LoginForm, RegisterForm, CommentForm, EditProfileForm, EditAccountForm
from django.views.generic import ListView, DetailView, CreateView,  UpdateView, DeleteView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from .tests import get_client_ip


# def index_view(request):
#
#     contents = VideoContent.objects.all()
#
#     context = {
#         'title': 'Main page',
#         'contents' : contents
#     }
#
#     return render(request, 'uzbektube/index.html', context )
#
#

class ContentListView(ListView):
    model = VideoContent
    context_object_name = 'contents'
    template_name = 'uzbektube/index.html'
    extra_context = {
        'title': 'Главная страница'
    }


# =====================================================================
# def get_category_content(request, category_id):
#     contents = VideoContent.objects.filter(category=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'contents': contents,
#         'title': category.title
#     }
#
#
#     return render(request, 'uzbektube/index.html', context)

class ContentByCategory(ContentListView):
    def get_queryset(self):
        contents = VideoContent.objects.filter(category=self.kwargs['category_id'])
        return contents

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(id=self.kwargs['category_id'])
        context['title'] = category.title

        return context


# =====================================================================

# def video_content_detail(request, pk):
#     video = VideoContent.objects.get(pk=pk)
#
#     context = {
#         'title': video.title,
#         'content': video,
#     }
#
#     return render(request, 'uzbektube/videocontent_detail.html', context)

class VideoContentDetail(DetailView):
    model = VideoContent
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content = self.object  # VideoContent instance from DetailView
        context['title'] = content.title
        context['items'] = VideoContent.objects.all()[::1]
        context['comment_form'] = CommentForm()  # Add form for adding comments
        context['comments'] = Comment.objects.filter(content=content).order_by('-created_at')

        # View tracking logic
        ip = get_client_ip(self.request)
        if Ip.objects.filter(ip=ip).exists():
            content.views.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            content.views.add(Ip.objects.get(ip=ip))

        # Pass the comment instance for editing when needed
        comment_pk = self.request.GET.get('edit_comment')  # Get comment pk from the query string if we want to edit
        if comment_pk:
            comment = Comment.objects.get(pk=comment_pk)
            context['comment_form'] = CommentForm(instance=comment)  # Populate form with comment instance

        return context



# =====================================================================
# def add_new_content(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             content = VideoContent.objects.create(**form.cleaned_data)
#             content.save()
#             return redirect('content', content.pk)
#         else:
#             return redirect('add_content')
#
#     else:
#         form = VideoForm()
#
#     context = {
#         'title': 'content',
#         'form': form
#     }
#
#     return render(request, 'uzbektube/add_content.html', context)

class NewContent(LoginRequiredMixin, CreateView):
    form_class = VideoForm
    template_name = 'uzbektube/add_content.html'
    login_url = 'login'
    extra_context = {
        'title': 'Добавить контент'
    }

    # def get(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('login')
    #     else:
    #         return super(NewContent, self).get( request, *args, **kwargs)


def user_login_vew(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:

        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    return redirect('main')
        else:
            form = LoginForm()
        context = {
            'title': 'Авторизация',
            'form': form
        }
        return render(request, 'uzbektube/login.html', context)


def user_logout_view(request):
    logout(request)

    return redirect('main')


def register_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()

                return redirect('login')
        else:
            form = RegisterForm()

        context = {
            'title': 'Регистрация',
            'form': form
        }

        return render(request, 'uzbektube/register.html', context)


def comment_save_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.content = VideoContent.objects.get(pk=pk)
            comment.user = request.user
            comment.save()
            return redirect('content', pk)


def comment_delete(request, pk):
    if request.user.is_authenticated:
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.user == request.user:
                comment.delete()

            return redirect('content', comment.content.pk)
        except:
            return redirect('main')


class SearchContent(ContentListView):
    def get_queryset(self):
        word = self.request.GET.get('q')
        contents = VideoContent.objects.filter(title__iregex=word)[::-1]
        return contents


def profile_view(request, pk):
    try:
        user = User.objects.get(id=pk)
        if user:
            profile = Profile.objects.get(user=user)
            contents = VideoContent.objects.filter(author=user)

            context = {
                'title': 'User Profile',
                'contents': contents,
                'profile': profile
            }

            return render(request, 'uzbektube/profile.html', context)

        else:
            return redirect('main')
    except:
        return redirect('main')


def edit_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return redirect('profile', request.user.pk)
        else:
            form = EditProfileForm(instance=request.user.profile)

        context = {
            'title': 'Change Profile',
            'form': form
        }

        return render(request, 'uzbektube/edit.html', context)



def edit_account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = EditAccountForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                data = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                if data['old_password'] and user.check_password(data['old_password']):
                    if data['old_password'] and data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)

                        return redirect('profile', user.id)
                    else:
                        return redirect('edit_account')
                else:
                    return redirect('profile', user.id)



        else:
            form = EditAccountForm(instance=request.user)

        context = {
            'title': 'Change Account',
            'form': form
        }

        return render(request, 'uzbektube/edit.html', context)


class UpdateContentview(LoginRequiredMixin, UpdateView):
    model = VideoContent
    form_class = VideoForm
    login_url = 'login'
    template_name = 'uzbektube/add_content.html'
    extra_context = {
        'title': 'Edit video'
    }

    def get(self, request, *args, **kwargs):
        content = VideoContent.objects.get(pk=self.kwargs['pk'])
        if content.author == request.user:
            return super(UpdateContentview, self).get(request, *args, **kwargs)
        else:
            return redirect('main')

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


class DeleteContentView(LoginRequiredMixin, DeleteView):
    model = VideoContent
    login_url = 'login'
    context_object_name = 'content'
    extra_context = {
        'title': 'Delete video'
    }

    def get(self, request, *args, **kwargs):
        content = VideoContent.objects.get(pk=self.kwargs['pk'])
        if content.author == request.user:
            return super(DeleteContentView, self).get(request, *args, **kwargs)
        else:
            return redirect('main')

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})



class UpdateCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'uzbektube/components/_update_comment.html'
    login_url = 'login'
    context_object_name = 'comment'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.get_form()
        context['is_update'] = True
        return context

    def get(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        if comment.user == request.user:
            return super(UpdateCommentView, self).get(request, *args, **kwargs)
        else:
            return redirect('main')

    def get_success_url(self):
        return reverse('content', kwargs={'pk': self.object.content.pk})
