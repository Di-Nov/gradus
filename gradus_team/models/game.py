from django.db import models
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

    guest_team = models.ForeignKey('Team', verbose_name='Гостевая команда',
                                   related_name='game_guest',
                                   on_delete=models.PROTECT,
                                   )

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус игры')
    data = models.DateTimeField(blank=True, verbose_name='Дата и время матча')

    objects = models.Manager()
    published_games = PublishedGameManager()

    def __str__(self):
        return (f'{self.home_team.name} {self.game_goal.filter(team_goal=self.home_team).count()}:'
                f'{self.game_goal.filter(team_goal=self.guest_team).count()} {self.guest_team.name} | {self.data.date()} {self.data.hour}:{self.data.minute}')

        # return (f'{self.home_team.name} {Goal.objects.filter(game_goal=self).filter(time_goal=self.home_team)}:'
        #         f'{Goal.objects.filter(game_goal=self).filter(time_goal=self.guest_team)}:{self.guest_team.name}')

    def get_absolute_url(self):
        return reverse('gradus_team:show_game', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
