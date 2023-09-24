from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
class Courses(models.Model):
    name=models.CharField(max_length=150, unique=True)
    startTime=models.DateTimeField(null=True)
    endTime=models.DateTimeField(null=True)
    duration=models.IntegerField(null=True)
    def __str__(self):
        return self.name
    
class CourseUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_course')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='course_users')

