from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from gradus_team.models.game import Game
from gradus_team.models.player import Player
from gradus_team.models.team import Team


class YellowCard(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_yellow_card',
                               verbose_name='Игрок')
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name='game_yellow_card',
                             verbose_name='Игра')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_yellow_card',
                             verbose_name='Команда')
    time_yellow_card = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, 'Минимальное значение 1'),
        MaxValueValidator(50, 'Максимальное значение 50'),
    ],
        verbose_name='Минута ЖК')

    def save(self, *args, **kwargs):
        self.team = self.player.team
        super().save(*args, **kwargs)
