from django.urls import path
from . import views
from django.contrib.auth import views as auth_login

urlpatterns = [
    path('all/', views.GetAllPostsView.as_view(), name="get_all_posts"),

    path('upload/', views.UploadPostsView.as_view(), name="upload_posts"),

    path('view-posts/<str:id>', views.ViewPostsView.as_view(), name="view_posts"),

    path('view-own-posts/', views.ViewOwnPostsView.as_view(), name="view_own_posts"),


]