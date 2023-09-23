from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('courses', views.CoursesViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('validate_token/', views.validate_token, name='validate_token'),
    path('reset_password/', views.reset_password, name='reset_password'),
]
