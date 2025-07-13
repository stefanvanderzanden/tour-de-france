from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.views.generic.base import RedirectView

from apps.games.models import ParticipantTeam, RiderForParticipantTeam, StageScoreForParticipantTeam
from apps.races.models import Round, TeamForRound, RiderForTeam, StageDay


class RoundContextMixin:
    """Mixin to add round and year context from URL parameters"""
    def get_context_data(self, **kwargs):
        return {
            "round": self.kwargs.get('round'),
            "year": self.kwargs.get('year'),
        }

    def get_round_object(self):
        """Helper method to get the Round object from URL parameters"""
        return get_object_or_404(
            Round,
            type=self.kwargs["round"],
            year=self.kwargs["year"]
        )

    def get_participant_team(self):
        """Helper method to get the user's participant team for this round"""
        round_obj = self.get_round_object()
        return ParticipantTeam.objects.get(
            user=self.request.user,
            round=round_obj
        )


class StartRoundView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        round_type = kwargs.get("round")
        year = kwargs.get("year")

        round_obj = Round.objects.get(type=round_type, year=year)

        ParticipantTeam.objects.get_or_create(
            user=request.user,
            round=round_obj
        )

        return redirect('games:dashboard', round=round_type, year=year)


class RoundDetailView(RoundContextMixin, TemplateView):
    """Main dashboard showing user's team with 27 slots"""
    template_name = 'games/round_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get or create user's team
        participant_team = self.get_participant_team()

        # Create 27 slots (some filled, some empty)
        selected_riders = RiderForParticipantTeam.objects.filter(
            participant_team=participant_team
        ).select_related("rider").order_by("position")
        rider_by_position = {r.position: r for r in selected_riders}
        round = self.get_round_object()
        can_change = not round.has_started

        context.update({
            "can_change": True,
            'participant_team': participant_team,
            'rider_by_position': rider_by_position,
            'riders_count': len(selected_riders),
        })
        return context


class RiderSelectionModalView(RoundContextMixin, LoginRequiredMixin, View):
    """Modal view for selecting riders"""
    template_name = 'games/rider_selection_modal.html'

    def get(self, request, *args, **kwargs):
        """Display available riders in modal"""
        # Get user's team using the mixin helper
        round_obj = self.get_round_object()
        participant_team = self.get_participant_team()
        selected_rider_ids = participant_team.riders.values_list('id', flat=True)

        # Get all active riders for this round
        teams_for_round = TeamForRound.objects.filter(round=round_obj).values_list("team_id", flat=True)
        riders = RiderForTeam.objects.filter(is_active=True, team__in=teams_for_round)

        # Add search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            riders = riders.filter(
                Q(rider__first_name__icontains=search_query) |
                Q(rider__last_name__icontains=search_query) |
                Q(team__team__name__icontains=search_query)
            )

        # Filter by team if specified
        team_filter = request.GET.get('team', '')
        if team_filter:
            riders = riders.filter(team__id=team_filter)

        # Get all teams for filter dropdown
        teams = TeamForRound.objects.all().order_by('order')

        context = self.get_context_data(**kwargs)
        shown_riders = []
        if search_query or team_filter:
            # Only show riders if filter is active
            shown_riders = riders.order_by("team__order", "number")

        context.update({
            'riders': shown_riders,
            'teams': teams,
            'selected_rider_ids': list(selected_rider_ids),
            'participant_team': participant_team,
            'search_query': search_query,
            'team_filter': team_filter,
            'position': kwargs.get("position"),
        })

        return render(request, self.template_name, context)


class AddRiderView(LoginRequiredMixin, RoundContextMixin, View):
    """Handle adding a rider to user's team"""

    def post(self, request, *args, **kwargs):
        """Add rider to user's team"""
        rider_id = request.POST.get("rider_id")
        position = request.POST.get("position")
        rider_for_team = get_object_or_404(
            RiderForTeam,
            id=rider_id,
            is_active=True
        )
        participant_team = self.get_participant_team()

        try:
            participant_team.add_rider(rider_for_team, position)

            response = HttpResponse("")
            response["HX-Trigger"] = "refreshTeam, closeModal"
            return response

        except ValidationError as e:
            # Return error response
            return JsonResponse({
                'error': True,
                'message': str(e)
            }, status=400)


class RemoveRiderView(LoginRequiredMixin, RoundContextMixin, View):
    """Handle removing a rider from user's team"""

    def post(self, request, *args, **kwargs):
        """Remove rider from user's team"""
        rider_id = kwargs.get('rider_id')
        rider_for_team = get_object_or_404(
            RiderForTeam,
            id=rider_id,
            is_active=True
        )
        participant_team = self.get_participant_team()

        try:
            participant_team.remove_rider(rider_for_team)

            # Return success response with HTMX trigger to refresh team
            response = HttpResponse("")
            response['HX-Trigger'] = 'refreshTeam, closeModal'
            return response

        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': 'Failed to remove rider'
            }, status=400)


class TeamSelectionPartialView(LoginRequiredMixin, RoundContextMixin, View):
    """Partial view to refresh just the team selection data"""

    def get(self, request, *args, **kwargs):
        """Return updated team slots HTML"""
        participant_team = self.get_participant_team()
        selected_riders = RiderForParticipantTeam.objects.filter(
            participant_team=participant_team
        ).select_related("rider").order_by("position")
        rider_by_position = {r.position: r for r in selected_riders}

        context = self.get_context_data(**kwargs)
        context.update({
            "can_change": True,
            'rider_by_position': rider_by_position,
            'participant_team': participant_team,
        })

        return render(request, 'games/partials/team_selection.html', context)


class RoundSubleagueOverview(LoginRequiredMixin, RoundContextMixin, TemplateView):
    template_name = "games/round_subleague_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round = self.get_round_object()

        # Get all races with scores
        stage_days = StageDay.objects.filter(round=round, scores_for_riders__isnull=False).distinct().order_by("number")

        labels = [s.number for s in stage_days]
        data_sets = []

        for participant_team in ParticipantTeam.objects.all():
            data_set = {
                "data": [],
                "label": participant_team.user.get_full_name(),
            }
            accumulated_score = 0
            for stage_day in stage_days:
                try:
                    stage_score = StageScoreForParticipantTeam.objects.get(
                        participant_team=participant_team, stage=stage_day
                    )
                    accumulated_score = stage_score.accumulated_score
                except StageScoreForParticipantTeam.DoesNotExist:
                    pass

                data_set["data"].append(accumulated_score)

            data_sets.append(data_set)

        context["chart_data"] = {
            "labels": labels,
            "datasets": data_sets
        }
        return context