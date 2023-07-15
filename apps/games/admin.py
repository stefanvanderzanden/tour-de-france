from django.contrib import admin

from apps.games.models import *


@admin.register(ScoreTableEntryForRound)
class ScoreTableEntryForRoundAdmin(admin.ModelAdmin):
    fields = ["round", "position", "score"]
    list_display = ["round", "position", "score"]


class ParticipantTeamRidersTabularInline(admin.TabularInline):
    model = ParticipantTeam.riders.through
    extra = 22


# class ScoreForStageForParticipantTeamTabularInline(admin.TabularInline):
#     model = ParticipantTeam.stage_scores.through


@admin.register(ParticipantTeam)
class ParticipantTeamAdmin(admin.ModelAdmin):
    fields = ["user", "round"]
    list_display = ["user", "round"]
    inlines = (ParticipantTeamRidersTabularInline, )


# class ScoreForRiderForStageTabularInline(admin.TabularInline):
#     model = ScoreForRiderForStage
#     extra = 10
#

# @admin.register(StageScore)
# class StageScoreAdmin(admin.ModelAdmin):
#     fields = ["stage"]
#     list_display = ["stage"]
#     list_filter = ["stage"]
#     inlines = (ScoreForRiderForStageTabularInline,)


class RiderStageScoresTabularInline(admin.TabularInline):
    model = StageScoreForParticipantTeam.rider_stage_scores.through
    extra = 1


@admin.register(StageScoreForParticipantTeam)
class ScoreForStageForParticipantTeamAdmin(admin.ModelAdmin):
    fields = ["participant_team", "stage", "score_for_stage", "accumulated_score"]
    list_display = ["participant_team", "stage", "score_for_stage", "accumulated_score"]
    list_filter = ["stage", "participant_team"]
    inlines = (RiderStageScoresTabularInline,)
