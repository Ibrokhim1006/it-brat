from django.db import models
from authen.models import CustomUser


class Heading(models.Model):
    name = models.CharField(max_length=250, verbose_name='Рубрику')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "heading"
        verbose_name = "Рубрику"
        verbose_name_plural = "Рубрику"


class ResumeModel(models.Model):
    contact = models.CharField(max_length=250, verbose_name='Контактная информация')
    experience = models.IntegerField(verbose_name='Опыт работы')
    hard_skills = models.JSONField(verbose_name='Hard skills', null=True, blank=True)
    soft_skills = models.JSONField(verbose_name='Soft Skills', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='resume/', null=True, blank=True)
    heading = models.ForeignKey(Heading, on_delete=models.CASCADE, verbose_name='Рубрику')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор', related_name='resume')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Рубрику: {self.heading.name} - Автор: {self.owner.username}'
    
    class Meta:
        db_table = "resume_model"
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"


class FavoritesResume(models.Model):
    resume = models.ForeignKey(ResumeModel, on_delete=models.CASCADE, null=True, blank=True, related_name="favorite")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"Автор: {self.owner.username}"
    
    class Meta:
        db_table = "favorites_resume"
        verbose_name = "Избранно резюме"
        verbose_name_plural = "Избранно резюме"


class NotificationResume(models.Model):
    favorite = models.ForeignKey(FavoritesResume, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)