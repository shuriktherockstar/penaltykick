from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Article(models.Model):
    LEAGUE_CHOICES = [
        ('rus1', 'Российская Премьер-лига'),
        ('eng1', 'Английская Премьер-лига'),
        ('esp1', 'Ла Лига'),
        ('ger1', 'Бундеслига'),
        ('ita1', 'Серия А'),
        ('fra1', 'Лига 1')
    ]

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=150)
    content = models.TextField()
    date_published = models.DateTimeField(default=timezone.now)
    league = models.CharField(max_length=4, choices=LEAGUE_CHOICES)
    image = models.ImageField(upload_to='articles/', null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class Video(models.Model):
    title = models.CharField(max_length=1000)
    link = models.URLField()
    date_uploaded = models.DateTimeField(default=timezone.now)