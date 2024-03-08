from django.db import models
from django.db.models import Q
from django.urls import reverse


class PublishedGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Game.Status.PUBLISHED)


class Game(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    home_team = models.ForeignKey('Team', verbose_name='Домашняя команда',
                                  related_name='game_home',
                                  on_delete=models.PROTECT,
                                  )
    goals_home_team = models.PositiveSmallIntegerField(default=0, verbose_name='Голов домашней команды')

    guest_team = models.ForeignKey('Team', verbose_name='Гостевая команда',
                                   related_name='game_guest',
                                   on_delete=models.PROTECT,
                                   )
    goals_guest_team = models.PositiveSmallIntegerField(default=0, verbose_name='Голов гостевой команды')

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус игры')
    data = models.DateTimeField(blank=True, verbose_name='Дата и время матча')

    objects = models.Manager()
    published_games = PublishedGameManager()

    def __str__(self):
        return f'{self.home_team.name} {self.goals_home_team}:{self.goals_guest_team} {self.guest_team.name}'

    def get_absolute_url(self):
        return reverse('gradus_team:show_game', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.goals_home_team = self.game_goal.filter(Q(team_goal=self.home_team, own_goal=False) | Q(self.game_goal.filter(team_goal=self.guest_team, own_goal=True))).count()
        self.goals_guest_team = self.game_goal.filter(Q(team_goal=self.guest_team, own_goal=False) | Q(self.game_goal.filter(team_goal=self.home_team, own_goal=True))).count()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
