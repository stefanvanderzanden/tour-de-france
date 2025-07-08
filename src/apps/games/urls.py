from django.urls import path
from django.urls.conf import include
from django.urls.converters import register_converter, StringConverter

from apps.games.views import (
    RiderSelectionModalView,
    AddRiderView,
    RemoveRiderView,
    RoundDetailView,
    TeamSelectionPartialView, StartRoundView
)
from ..races.models import Round

app_name = "games"

class RoundConverter(StringConverter):
    """Custom converter that only accepts valid round types"""

    # Create a regex pattern that matches only the valid round choices
    regex = '|'.join([choice[0] for choice in Round.ROUND_TYPE_CHOICES])

    def to_python(self, value):
        """Convert the URL parameter to Python value"""
        return str(value)

    def to_url(self, value):
        """Convert Python value back to URL parameter"""
        return str(value)

# Register the custom converter
register_converter(RoundConverter, 'round')

round_nested_patterns = [
    path("select-rider/<int:position>/", RiderSelectionModalView.as_view(), name="select_rider"),
    path("add-rider/", AddRiderView.as_view(), name="add_rider"),
    path("remove-rider/<int:rider_id>/", RemoveRiderView.as_view(), name="remove_rider"),
    path("team-selection-refresh/", TeamSelectionPartialView.as_view(), name="team_selection_refresh"),
]

urlpatterns = [
    path("<round:round>/<int:year>/start/", StartRoundView.as_view(), name="start"),
    path("<round:round>/<int:year>/", RoundDetailView.as_view(), name="round_detail"),
    path("<round:round>/<int:year>/", include(round_nested_patterns)),
]