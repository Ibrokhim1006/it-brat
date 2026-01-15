from django.db import models
from authen.models import CustomUser


class Conversation(models.Model):
    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='initiated_conversations', verbose_name='Инициатор')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='received_conversations', verbose_name='Получатель')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Time stamp', null=True, blank=True)

    def __str__(self) -> str:
        return f'Инициатор: {self.initiator.email} - Получатель: {self.receiver.email}'

    class Meta:
        db_table = "table_conversation"
        verbose_name = "Разговор"
        verbose_name_plural = "Разговор"


class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отправитель')
    text = models.CharField(max_length=200, blank=True, verbose_name='Сообщение')
    info = models.JSONField(null=True, blank=True, verbose_name='Информация')
    attachment = models.FileField(blank=True, null=True, verbose_name='Файл')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, verbose_name='Разговор', related_name='messages', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Time stamp', null=True, blank=True)

    def __str__(self) -> str:
        return f'Отправитель: {self.sender.email} - текст: {self.text}'
    
    class Meta:
        db_table = "chat_message"
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщение"


class NotificationChat(models.Model):
    favorite = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)


class Feedback(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    email = models.EmailField(verbose_name='E-mail')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Имя: {self.name} - Emil: {self.email}'
    
    class Meta:
        db_table = "feed_back"
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"


class Question(models.Model):
    text = models.CharField(max_length=500, verbose_name='Вопрос')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
    
    class Meta:
        db_table = "feedback"
        verbose_name = "ЗАДАТЬ ВОПРОС"
        verbose_name_plural = "ЗАДАТЬ ВОПРОС"


class Subscribe(models.Model):
    email = models.EmailField(verbose_name='E-mail')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Создать в')

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "subscrible"
        verbose_name = "Подпишись"
        verbose_name_plural = "Подпишись"


class Faq(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "faq"
        verbose_name = "Faq"
        verbose_name_plural = "Faq"