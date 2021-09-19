import os
from django.utils.timezone import now
from django.db import models as m
from authentication.models import User

class Chat(m.Model):
    name = m.CharField('Название', max_length=50)

    def calculateMessages(self):
        return Message.objects.filter(mto=self, read_status=1).count()

    unread = property(calculateMessages)

    def __str__(self):
        return self.name

class Message(m.Model):
    sender = m.ForeignKey(User, on_delete=m.CASCADE, verbose_name='Отправитель')
    receiver = m.ForeignKey(Chat, on_delete=m.CASCADE, verbose_name='Получатель')
    text = m.TextField('Сообщение', blank=False)
    time = m.DateTimeField('Время отправления', default=now, editable=False)
    read_status = m.BooleanField('Статус')

    def __str__(self):
        return self.text

class Chat_User(m.Model):
    chat = m.ForeignKey(Chat, on_delete=m.CASCADE, related_name="users")
    user = m.ForeignKey(User, on_delete=m.CASCADE, related_name="chats")

    class Meta:
        unique_together = ('chat', 'user',)

    def __str__(self):
        return str(self.chat) + '-' + str(self.user)
