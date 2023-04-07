from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, TemplateView, DeleteView

from .forms import *
from .models import *


# О сайте
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


# Вход пользователя на сайт
class ArticleLoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'
    success_message = 'You have successfully sign in'


# Выход
class ArticleLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


# Смена данных пользователя
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Personal data has been successfully changed'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# Смена пароля
class ArticlePasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'User password changed successfully'


# Регистрация пользователя
class RegisterUserView(CreateView):
    model = User
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


# Удаление пользователя
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')


    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# список всех записей по рубрикам меню (динамическая)
def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Article.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {
        'rubric': rubric,
        'page': page,
        'bbs': page.object_list,
        'form': form,
    }

    return render(request, 'main/by_rubric.html', context)

# Список записей пользователя
@login_required
def profile(request):
    bbs = Article.objects.filter(author=request.user.pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'bbs': page.object_list,
               'page': page,
               'paginator': paginator,
               'form': form}

    return render(request, 'main/profile.html', context)


# Главная
def index(request):
    bbs = Article.objects.filter(is_active=True)[:10]
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {
        'bbs': page.object_list,
        'page': page,
        'form': form,
    }
    return render(request, 'main/index.html', context)


# общая страница просмотра записи
def detail(request, rubric_pk, pk):
    bb = get_object_or_404(Article, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/detail.html', context)


# страница просмотра записи для пользователя
def profile_article_detail(request, rubric_pk, pk):
    bb = get_object_or_404(Article, pk=pk, author=request.user.pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/detail_article_detail.html', context)


# добавление записи
@login_required
def profile_article_add(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                return redirect('main:profile')
    else:
        form = ArticleForm(initial={'author': request.user.pk})
        formset = AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_article_add.html', context)


# редактирование записи
@login_required
def profile_article_change(request, pk):
    bb = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=bb)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                return redirect('main:profile')
    else:
        form = ArticleForm(instance=bb)
        formset = AIFormSet(instance=bb)
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_article_change.html', context)


# удаление записи
@login_required
def profile_article_delete(request, pk):
    bb = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        bb.delete()
        return redirect('main:profile')
    else:
        context = {'bb': bb, }
        return render(request, 'main/profile_article_delete.html', context)