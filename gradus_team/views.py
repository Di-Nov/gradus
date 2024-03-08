from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from gradus_team.models.game import Game
from gradus_team.models.goal import GoalAssist
from gradus_team.models.player import Player
from gradus_team.models.team import Team
from gradus_team.models.team_composition import TeamComposition
from gradus_team.models.yellow_card import YellowCard


class GradusHome(ListView):
    template_name = 'gradus/games/home.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.published_games.all().order_by('-data')


class ShowGame(DetailView):
    template_name = 'gradus/games/show_game.html'
    context_object_name = 'game'
    model = Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goals_HT'] = GoalAssist.objects.filter(
            Q(team_goal=context['game'].home_team, game_goal=context['game'], own_goal=False) | Q(
                team_goal=context['game'].guest_team, game_goal=context['game'], own_goal=True)).order_by('time_goal')
        context['goals_GT'] = GoalAssist.objects.filter(
            Q(team_goal=context['game'].guest_team, game_goal=context['game'], own_goal=False) | Q(
                team_goal=context['game'].home_team, game_goal=context['game'], own_goal=True)).order_by('time_goal')
        context['composition_HT'] = TeamComposition.objects.get(team=context['game'].home_team,
                                                                game=context['game']).composition
        context['composition_GT'] = TeamComposition.objects.get(team=context['game'].guest_team,
                                                                game=context['game']).composition
        context['yellow_card_HT'] = YellowCard.objects.filter(team=context['game'].home_team, game=context['game'])
        context['red_card_HT'] = YellowCard.objects.filter(team=context['game'].home_team, game=context['game'])
        return context


class ShowPlayer(DetailView):
    template_name = 'gradus/games/show_player.html'
    context_object_name = 'player'
    model = Player
    slug_field = 'slug'
    slug_url_kwarg = 'slug_player'


class ShowTeam(DetailView):
    template_name = 'gradus/games/show_team.html'
    context_object_name = 'team'
    model = Team
    slug_url_kwarg = 'slug_team'
    slug_field = 'slug_team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = context['team'].players
        return context
