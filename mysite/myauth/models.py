import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


def user_avatar_path(instance, filename):
    """Генерирует путь для сохранения аватарок пользователей"""
    return f'avatars/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(_("Аватар"), upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return f"Профиль {self.user.username}"


# Создание профиля при регистрации пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
