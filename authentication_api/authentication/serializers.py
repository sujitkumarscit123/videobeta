from rest_framework import serializers
from .models import Courses, CourseUsers


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseUsers
        fields = '__all__'
        depth=1
