from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter
)

from apps.races.models import *


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    fields = ["type", "start_date", "end_date"]
    list_display = ["type", "start_date", "end_date"]


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    fields = ["first_name", "last_name", "birth_date", "country"]
    list_display = ["last_name", "first_name", "birth_date", "country"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fields = ["name", "is_active"]
    list_display = ["name", "is_active"]


class RiderForTeamForRoundTabularInline(admin.TabularInline):
    model = TeamForRound.riders.through
    fields = ["rider", "number", "team_leader", "sprint_quality", "climb_quality", "attack_quality"]
    extra = 8


@admin.register(TeamForRound)
class TeamForRoundAdmin(admin.ModelAdmin):
    fields = ["team", "round"]
    list_display = ["team", "round"]
    list_filter = ["team__is_active"]
    inlines = (RiderForTeamForRoundTabularInline,)


class DayChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Day  # Optional, explicitly set here.
    base_fieldsets = (
        ("Standard info", {
            "fields": ("round", "date")
        }),
    )


@admin.register(RestDay)
class RestDayChildAdmin(DayChildAdmin):
    base_model = RestDay
    base_fieldsets = (
        (_("Gedeelde informatie"), {
            "fields": ("round", "date")
        }),
        (_("Rustdag informatie"), {
            "fields": ("number",)
        }),
    )
    show_in_index = False


class StageResultTabularInline(admin.TabularInline):
    model = StageResult
    fk_name = "stage"
    extra = 10


@admin.register(StageDay)
class StageDayChildAdmin(DayChildAdmin):
    list_display = ["number", "start_city", "end_city", "distance", "stage_type", "round"]
    base_model = StageDay
    base_fieldsets = (
        ("Standard info", {
            "fields": ("round", "date")
        }),
        (_("Etappe informatie"), {
            "fields": ("number", "start_city", "end_city", "distance", "stage_type")
        }),
    )
    show_in_index = False
    inlines = (StageResultTabularInline,)


@admin.register(Day)
class DayParentAdmin(PolymorphicParentModelAdmin):
    base_model = Day
    child_models = [RestDay, StageDay]
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ["date", "round", "polymorphic_ctype"]



# class RiderStageResultInline(admin.TabularInline):
#     model = RiderStageResult
#     extra = 10
#
#
# @admin.register(StageResult)
# class StageResultAdmin(admin.ModelAdmin):
#     fields = ["stage"]
#     list_display = ["stage"]
#     list_filter = ["stage"]
#     inlines = (RiderStageResultInline, )