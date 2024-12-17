# backend/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 在这里添加自定义字段
    # 例如：
    # phone_number = models.CharField(max_length=15, blank=True, null=True)

    # 为 groups 和 user_permissions 添加 related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # 修改这里
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # 修改这里
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )
