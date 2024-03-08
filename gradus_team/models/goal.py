from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from gradus_team.models.game import Game
from gradus_team.models.player import Player
from gradus_team.models.team import Team


class GoalAssist(models.Model):
    player_goal = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_goal',
                                    verbose_name='Автор мяча')
    player_assist = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='player_assist', verbose_name='Автор передачи')
    team_goal = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_goal',
                                  verbose_name='Команда')
    game_goal = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name='game_goal', verbose_name='Игра')
    time_goal = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, 'Минимальное значение 1'),
        MaxValueValidator(50, 'Максимальное значение 50'),
    ],
        verbose_name='Минута гола')

    def __str__(self):
        return f'{self.player_goal} - {self.game_goal}  ->> {self.time_goal} Минута'

    def save(self, *args, **kwargs):
        self.team_goal = self.player_goal.team
        super().save(*args, **kwargs)
