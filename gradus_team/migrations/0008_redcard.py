# Generated by Django 5.0.2 on 2024-03-08 15:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gradus_team', '0007_game_goals_guest_team_game_goals_home_team_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_red_card', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение 1'), django.core.validators.MaxValueValidator(50, 'Максимальное значение 50')], verbose_name='Минута ЖК')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='game_red_card', to='gradus_team.game', verbose_name='Игра')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_red_card', to='gradus_team.player', verbose_name='Игрок')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_red_card', to='gradus_team.team', verbose_name='Команда')),
            ],
        ),
    ]
