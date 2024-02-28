from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Player.Status.PUBLISHED)


class Game(models.Model):
    home_team = models.ForeignKey('Team', verbose_name='Домашняя команда',
                                  related_name='game_home',
                                  on_delete=models.PROTECT,
                                  )
    guest_team = models.ForeignKey('Team', verbose_name='Гостевая команда',
                                   related_name='game_guest',
                                   on_delete=models.PROTECT,
                                   )
    goal = models.ForeignKey('Goal', verbose_name='Гостевая команда',
                             related_name='game_goal',
                             on_delete=models.PROTECT,
                             )
    assist = models.ForeignKey('Assist', verbose_name='Голевые передачи',
                               related_name='game_assist',
                               on_delete=models.PROTECT,
                               )


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='Команда')
    logo = models.ImageField(upload_to='team_logo/%Y/%m', default=None, blank=True, null=True, verbose_name='Логотип')

    def __str__(self):
        return self.name


class Player(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    class Role(models.TextChoices):
        goalkeeper = 'G', 'Goalkeeper'
        left_defender = 'D', 'Defender'
        center_forward = 'F', 'Forward'

    name = models.CharField(max_length=255, verbose_name='Футболист')
    slug = models.SlugField(max_length=255, unique_for_date='publish', verbose_name='Слаг')
    description = models.TextField(blank=True, null=True, verbose_name='Биография')
    height = models.SmallIntegerField(blank=True, null=True, verbose_name='Рост')
    weight = models.SmallIntegerField(blank=True, null=True, verbose_name='Вес')
    team = models.ForeignKey('gradus_team.Team',
                             verbose_name='Команда',
                             related_name='player',
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

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    author = models.ForeignKey(get_user_model(),
                               related_name='blog_posts',
                               on_delete=models.CASCADE,
                               verbose_name='Автор')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gradus_team:player', kwargs={'id': self.id})

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Goal(models.Model):
    player_goal = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='goal', verbose_name='Автор мяча')
    time_goal = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, 'Минимальное значение 1'),
        MaxValueValidator(50, 'Максимальное значение 50'),
    ],
        verbose_name='Минута гола')


class Assist(models.Model):
    player_assist = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='assist' ,verbose_name='Автор мяча')
    time_assist = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, 'Минимальное значение 1'),
        MaxValueValidator(50, 'Максимальное значение 50'),
    ],
        verbose_name='Минута ассиста')
