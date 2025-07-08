from django.contrib import admin

from apps.games.models import *
from apps.races.models import StageDay


@admin.register(ScoreTableEntryForRound)
class ScoreTableEntryForRoundAdmin(admin.ModelAdmin):
    fields = ["round", "position", "score"]
    list_display = ["round", "position", "score"]


class ParticipantTeamRidersTabularInline(admin.TabularInline):
    model = ParticipantTeam.riders.through
    extra = 22


@admin.register(ParticipantTeam)
class ParticipantTeamAdmin(admin.ModelAdmin):
    fields = ["user", "round"]
    list_display = ["user", "round", "total_points"]
    actions = ["calculate_team_scores"]

    @admin.action(description="Bereken scores voor teams")
    def calculate_team_scores(modeladmin, request, queryset):
        # And now create the StageScoreForTeam
        for team in queryset:
            stages = StageDay.objects.filter(round=team.round)

            # First delete all StageScoreForParticipantTeam
            StageScoreForParticipantTeam.objects.filter(
                participant_team=team,
            ).delete()

            for stage in stages.order_by("number"):
                rider_scores = StageScoreForRider.objects.filter(
                    stage=stage,
                    rider__in=team.riders.all()
                )
                if not rider_scores.exists():
                    continue

                obj, created = StageScoreForParticipantTeam.objects.get_or_create(
                    participant_team=team,
                    stage=stage,
                )
                obj.rider_stage_scores.add(*rider_scores)
                stage_score =rider_scores.aggregate(score=Sum("score"))["score"]
                previous_scores = StageScoreForParticipantTeam.objects.filter(
                    participant_team=team,
                    stage__in=stages,
                    stage__number__lt=stage.number
                ).aggregate(
                    score_for_stage=Sum("score_for_stage")
                )["score_for_stage"] or 0
                obj.score_for_stage = stage_score
                obj.accumulated_score = stage_score + previous_scores
                obj.save()



class RiderStageScoresTabularInline(admin.TabularInline):
    model = StageScoreForParticipantTeam.rider_stage_scores.through
    extra = 1


@admin.register(StageScoreForParticipantTeam)
class ScoreForStageForParticipantTeamAdmin(admin.ModelAdmin):
    fields = ["participant_team", "stage", "score_for_stage", "accumulated_score"]
    list_display = ["participant_team", "stage", "score_for_stage", "accumulated_score"]
    list_filter = ["stage", "participant_team"]
    inlines = (RiderStageScoresTabularInline,)


@admin.register(StageScoreForRider)
class StageScoreForRiderAdmin(admin.ModelAdmin):
    fields = ["stage", "rider", "position", "score"]
    list_display = ["stage", "rider", "position", "score"]
    list_filter = ["stage", "rider"]
