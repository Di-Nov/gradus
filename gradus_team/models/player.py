import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedPlayersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Player.Status.PUBLISHED)


class Player(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    class Role(models.TextChoices):
        goalkeeper = 'G', 'Goalkeeper'
        left_defender = 'D', 'Defender'
        center_forward = 'F', 'Forward'

    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=255, blank=True, verbose_name='Отчество')
    slug = models.SlugField(max_length=255, unique_for_date='publish', verbose_name='Слаг')
    description = models.TextField(blank=True, null=True, verbose_name='Биография')
    height = models.SmallIntegerField(blank=True, null=True, verbose_name='Рост')
    weight = models.SmallIntegerField(blank=True, null=True, verbose_name='Вес')
    team = models.ForeignKey('gradus_team.Team',
                             verbose_name='Команда',
                             related_name='players',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             )
    age = models.SmallIntegerField(verbose_name='Возраст', blank=True, null=True)
    date_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    role = models.CharField(choices=Role.choices,
                            max_length=1,
                            null=True,
                            blank=True,
                            verbose_name='Роль'
                            )

    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    avatar = models.ImageField(upload_to='avatar/', default=None, blank=True, null=True, verbose_name='Фото')

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус игрока')
    author = models.ForeignKey(get_user_model(),
                               related_name='blog_posts',
                               on_delete=models.CASCADE,
                               verbose_name='Автор')

    objects = models.Manager()
    published_players = PublishedPlayersManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.team})'

    def get_absolute_url(self):
        return reverse('gradus_team:show_player', kwargs={'slug_player': self.slug})

    def save(self, *args, **kwargs):
        if not self.date_birth:
            self.age = None
        else:
            today = datetime.date.today()
            result = today.year - self.date_birth.year
            if today.month < self.date_birth.month or (
                    today.month == self.date_birth.month and today.day < self.date_birth.day):
                result -= 1
            self.age = result
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
