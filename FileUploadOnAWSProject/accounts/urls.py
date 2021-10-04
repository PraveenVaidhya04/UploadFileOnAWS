from django.urls import path
from . import views
from django.contrib.auth import views as auth_login

urlpatterns = [
    path('registration/', views.AccountRegistrationView.as_view(), name="account_registration"),

    path('login/', views.AccountLoginView.as_view(), name="account_login"),

    path('logout/', views.Logout.as_view(), name="account_logout"),
]