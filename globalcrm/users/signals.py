from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        # Здесь вы можете установить значения по умолчанию для полей профиля
        profile.name = "Имя по умолчанию"
        profile.surname = "Фамилия по умолчанию"
        profile.patronomic = "Отчество по умолчанию"
        profile.birth_date = "1990-07-30"
        profile.position = "Должность по умолчанию"
        profile.email = "Email по умолчанию"
        profile.phone = "Телефон по умолчанию"
        profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


