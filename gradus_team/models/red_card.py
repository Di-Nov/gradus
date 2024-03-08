from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from gradus_team.models.game import Game
from gradus_team.models.player import Player


class RedCard(models.Model):
    player_assist = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_red_card',
                                      verbose_name='Автор паса')
    game_assist = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name='game_red_card',
                                    verbose_name='Игра')
    time_assist = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, 'Минимальное значение 1'),
        MaxValueValidator(50, 'Максимальное значение 50'),
    ],
        verbose_name='Минута КК')