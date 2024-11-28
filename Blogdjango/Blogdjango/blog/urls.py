from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('create/', views.create_post_view, name='create_post'),
    path('post/edit/<int:post_id>/', views.edit_post_view, name='edit_post'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
]
