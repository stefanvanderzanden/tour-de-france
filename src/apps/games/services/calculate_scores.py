from django.db.models import Sum

from apps.races.models import StageDay, StageResult
from apps.games.models import (
    ParticipantTeam,
    ScoreTableEntryForRound,
    StageScoreForRider, StageScoreForParticipantTeam
)


class CalculateScoresService:

    def __init__(self):
        # TODO: set repositories
        pass

    @staticmethod
    def create_rider_stage_results(stage: StageDay):
        stage_results = StageResult.objects.filter(stage=stage)

        # Calculate `games.RiderScoreForStage`
        for result in stage_results:
            position = result.position
            table_entry = ScoreTableEntryForRound.objects.get(
                round=stage.round,
                position=position
            )
            StageScoreForRider.objects.update_or_create(
                stage=stage,
                rider=result.rider,
                position=position,
                defaults={
                    "score": table_entry.score
                }
            )

    @staticmethod
    def create_participant_team_scores(stage: StageDay):
        active_teams = ParticipantTeam.objects.filter(round=stage.round)
        for team in active_teams:
            scores_for_rider = StageScoreForRider.objects.filter(
                stage=stage,
                rider__in=team.riders.all()
            )
            total_for_stage = scores_for_rider.aggregate(total=Sum("score")).get("total") or 0
            accumulated_for_stage = StageScoreForParticipantTeam.objects.filter(
                participant_team=team,
                stage__date__lt=stage.date
            ).aggregate(total=Sum("rider_stage_scores__score")).get("total") or 0

            participant_team_score, created = StageScoreForParticipantTeam.objects.update_or_create(
                participant_team=team,
                stage=stage,
                defaults={
                    "score_for_stage": total_for_stage,
                    "accumulated_score": accumulated_for_stage + total_for_stage
                }
            )
            participant_team_score.rider_stage_scores.set(scores_for_rider)

