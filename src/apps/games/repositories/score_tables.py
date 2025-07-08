from apps.games.models import ScoreTableEntryForRound


class ScoreTableRepository:

    @staticmethod
    def get_score_table_by_id(table_id):
        return ScoreTableEntryForRound.objects.get(pk=table_id)

    @staticmethod
    def get_score_table_by_position_round(position, round_id):
        return ScoreTableEntryForRound.objects.get(
            round_id=round_id,
            position=position
        )

    @staticmethod
    def create_score_table(round_id, position, score):
        return ScoreTableEntryForRound.objects.create(
            round_id=round_id,
            position=position,
            score=score
        )