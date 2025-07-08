from apps.games.models import ParticipantTeam


class ParticipantTeamRepository:

    @staticmethod
    def get_participant_team_by_id(team_id):
        return ParticipantTeam.objects.get(pk=team_id)

    @staticmethod
    def create_participant_team(user_id):
        return ParticipantTeam.objects.create(user_id=user_id)