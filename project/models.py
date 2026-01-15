from django.db import models
from authen.models import CustomUser


class CategoriyaProject(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    logo = models.ImageField(upload_to='category/', verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category_project"
        verbose_name = "Категория проекта"
        verbose_name_plural = "Категория проекта"


class Project(models.Model):
    VALUTA = (
        (1, 'Руб'),
        (2, 'Долл'),
    )
    name = models.CharField(max_length=250, verbose_name='Название проекта')
    contact = models.CharField(max_length=250, verbose_name='Контакт')
    valuta = models.IntegerField(choices=VALUTA, default=1, verbose_name='Валюта')
    price = models.IntegerField(verbose_name='Цена')
    skils = models.JSONField(verbose_name='Навыки', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='project/', verbose_name='Изображение')
    category = models.ForeignKey(CategoriyaProject, on_delete=models.CASCADE, verbose_name='Категория')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Проект: {self.name} - Автор: {self.owner.username}'
    
    class Meta:
        db_table = "project"
        verbose_name = "Проект"
        verbose_name_plural = "Проект"


class FavoritesProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="favorite")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Проект: {self.project.name}"
    
    class Meta:
        db_table = "favorites_project"
        verbose_name = "Избранно проекте"
        verbose_name_plural = "Избранно проекте"


class Notification(models.Model):
    favorite = models.ForeignKey(FavoritesProject, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
