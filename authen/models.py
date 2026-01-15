from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    STATUS = (
        (1, 'Активно ищу работу'),
        (2, 'Работаю над проектом'),
    )
    status = models.IntegerField(choices=STATUS, default=1)