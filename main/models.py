from django.db import models
from main.tasks import *
from django.dispatch import receiver
from django.db.models.signals import post_save


class Created(models.Model):
    """
    Нужен для того, чтобы во всех моделях не прописывать одно и тоже поле, все последующие модели будут наследоваться
    от этого класса и будут принимать его поля
    """
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Значение abstract = True означает что при создании файлов миграции для нашей модели эти файлы не будут
        создаваться
        """
        abstract = True


class Problem(Created):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='problems')

    def __str__(self) -> str:
        return self.title


class Picture(Created):
    image = models.ImageField(
        upload_to='pictures'
    )
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='pictures')


class Reply(Created):
    text = models.TextField()
    image = models.ImageField(upload_to='reply_pictures')
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='replies')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.text[:10] + '...'


class Comment(Created):
    text = models.TextField()
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text[:10] + '...'


@receiver(post_save, sender=Problem)
def notify_user(sender, instance, created, **kwargs):
    if created:
        email = instance.author.email
        notify_user_func.delay(email)
