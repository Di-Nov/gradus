from django.contrib import admin, messages
from django.db.models import Avg, Count

from .models.game import Game
from .models.goal import GoalAssist
from .models.player import Player
from .models.team import Team
from .models.team_composition import TeamComposition
from .models.yellow_card import YellowCard

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['home_team', 'goals_home_team', 'guest_team', 'goals_guest_team', 'data']
    list_display_links = ['home_team', ]
    exclude = ['goals_home_team', 'goals_guest_team']
    list_per_page = 20
    save_on_top = True


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['player_FIO', 'team', 'age', 'date_birth', 'role', 'status', ]
    list_editable = ['team']
    prepopulated_fields = {"slug": ["last_name", 'first_name']}
    list_display_links = ['player_FIO', ]
    list_filter = ['team', 'status', 'role']
    list_per_page = 10
    search_fields = ['first_name__icontains', 'last_name__icontains', 'team__name']
    save_on_top = True
    actions = ['make_published', 'make_draft']
    exclude = ['age']

    @admin.display(description='Игрок')
    def player_FIO(self, player: Player):
        return player

    # @admin.display(description='Голы', empty_value=0)
    # def count_goals(self, obj: Player):
    #     return obj.player_assist.count()

    # @admin.display(description='Голевые передачи')
    # def count_assists(self, obj):
    #     results = obj.player_assist.count()
    #     return results

    @admin.action(description='Сделать действующими')
    def make_published(self, request, queryset):
        count = queryset.update(status=Player.Status.PUBLISHED)
        self.message_user(request, f"{count} игрока(ов) стали активны.", messages.WARNING)

    @admin.action(description='Сделать недействующим')
    def make_draft(self, request, queryset):
        count = queryset.update(status=Player.Status.DRAFT)
        self.message_user(request, f"{count} игрока(ов) стали неактивны.", messages.WARNING)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'count_players', 'avg_age', 'status']
    prepopulated_fields = {"slug_team": ["name"]}
    list_display_links = ['name', ]
    list_filter = ['name']
    list_per_page = 20
    search_fields = ['name']
    save_on_top = True

    @admin.display(description='Средний возраст')
    def avg_age(self, team: Team):
        result = team.players.aggregate(avg_age=Avg('age'))
        return result['avg_age']

    @admin.display(description='Количество игроков')
    def count_players(self, team: Team):
        return team.players.count()



@admin.register(TeamComposition)
class TeamCompositionAdmin(admin.ModelAdmin):
    list_display = ['game', 'team']
    list_display_links = ['game', ]
    list_per_page = 20
    save_on_top = True
    filter_horizontal = ['composition']

@admin.register(GoalAssist)
class GoalAssistAdmin(admin.ModelAdmin):
    list_display = ['player_goal', 'player_assist', 'game_goal', 'time_goal']
    list_display_links = ['player_goal', ]
    list_filter = ['team_goal']
    exclude = ['team_goal']
    list_per_page = 20
    save_on_top = True
    autocomplete_fields = ['player_goal', 'player_assist']

@admin.register(YellowCard)
class GoalAssistAdmin(admin.ModelAdmin):
    list_display = ['player', 'game', 'team', 'time_yellow_card']
    list_display_links = ['player', ]
    exclude = ['team']
    list_per_page = 20
    save_on_top = True
    autocomplete_fields = ['player', ]