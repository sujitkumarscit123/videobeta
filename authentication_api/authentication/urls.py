from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('validate_token/', views.validate_token, name='validate_token'),
    path('reset_password/', views.reset_password, name='reset_password'),
]
