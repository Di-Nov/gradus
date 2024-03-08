from django.db import models
from django.urls import reverse


class PublishedTeamsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Team.Status.PUBLISHED)


class Team(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    name = models.CharField(max_length=100, verbose_name='Команда')
    slug_team = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='team_logo/%Y/%m', default=None, blank=True, null=True, verbose_name='Логотип')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус команды')

    objects = models.Manager()
    published_teams = PublishedTeamsManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_team', kwargs={'slug_team': self.slug_team})


    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
