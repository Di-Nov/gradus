from django.db import models

from gradus_team.models.game import Game


class TeamComposition(models.Model):
    composition = models.ManyToManyField('Player', blank=True, related_name='composition',
                                         verbose_name='Состав команды')
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='game_composition',
                             verbose_name='Игра')
    team = models.ForeignKey('Team', on_delete=models.PROTECT, related_name='team_composition',
                             verbose_name='Команда')

    class Meta:
        verbose_name = 'Состав команды'
        verbose_name_plural = 'Составы команд'
