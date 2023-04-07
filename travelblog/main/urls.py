from django.urls import path

from .views import *

app_name = 'main'
urlpatterns = [
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('account/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('account/register/', RegisterUserView.as_view(), name='register'),
    path('account/login/', ArticleLoginView.as_view(), name='login'),
    path('account/logout/', ArticleLogoutView.as_view(), name='logout'),
    path('account/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('account/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('account/profile/change/<int:pk>/', profile_article_change, name='profile_bb_change'),
    path('account/profile/delete/<int:pk>/', profile_article_delete, name='profile_bb_delete'),
    path('account/profile/add/', profile_article_add, name='profile_bb_add'),
    path('account/profile/<int:pk>/', profile_article_detail, name='profile_bb_detail'),
    path('account/profile/', profile, name='profile'),
    path('account/password/change/', ArticlePasswordChangeView.as_view(), name='password_change'),
    path('', index, name='index'),

]