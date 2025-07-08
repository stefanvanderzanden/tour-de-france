from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.aggregates import Sum
from django.utils.translation import gettext_lazy as _


class ScoreTableEntryForRound(models.Model):
    round = models.ForeignKey("races.Round", on_delete=models.PROTECT, verbose_name=_("Ronde"))
    position = models.IntegerField(
        verbose_name=_("Positie"),
    )
    score = models.IntegerField(
        verbose_name=_("Score")
    )

    class Meta:
        verbose_name = _("Score tabel regel")
        verbose_name_plural = _("Score tabel regels")
        ordering = ("round", "position")

    def __str__(self):
        return _("Tabel regel voor positie %(number)s voor %(round)s ") % {
            "number": self.position,
            "round": self.round
        }


class ParticipantTeam(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.PROTECT, verbose_name=_("Gebruiker"))
    round = models.ForeignKey("races.Round", on_delete=models.PROTECT, verbose_name=_("Ronde"))
    riders = models.ManyToManyField(
        "races.RiderForTeam",
        through="games.RiderForParticipantTeam",
        verbose_name=_("Riders"),
        blank=True
    )
    # stage_scores = models.ManyToManyField(
    #     "games.StageScoreForRider",
    #     verbose_name=_("Etappe score voor renner"),
    #     blank=True
    # )

    class Meta:
        verbose_name = _("Speelteam")
        verbose_name_plural = _("Speelteams")
        unique_together = ("user", "round")

    def __str__(self):
        return _("Team van %(user)s voor %(round)s") % {
            "user": self.user.get_full_name(),
            "round": self.round
        }

    @property
    def rider_count(self):
        return self.riders.count()

    @property
    def remaining_slots(self):
        return 27 - self.rider_count

    @property
    def total_points(self):
        return StageScoreForParticipantTeam.objects.filter(
            participant_team=self,
            stage__round=self.round,
        ).aggregate(
            score=Sum("score_for_stage")
        )["score"]

    @property
    def total_price(self):
        return sum(rider.price for rider in self.riders.all())

    def can_add_rider(self):
        return self.rider_count < 27

    def add_rider(self, rider, position):
        """Add a rider to the team if possible"""
        if not self.can_add_rider():
            raise ValidationError("Team is full. Cannot add more riders.")

        if rider in self.riders.all():
            raise ValidationError("Rider is already in your team.")

        if not rider.is_active:
            raise ValidationError("This rider is not available for selection.")

        RiderForParticipantTeam.objects.create(
            participant_team=self,
            rider=rider,
            position=position
        )

        return True

    def remove_rider(self, rider):
        """Remove a rider from the team"""
        self.riders.remove(rider)
        return True


class RiderForParticipantTeam(models.Model):
    participant_team = models.ForeignKey(
        "games.ParticipantTeam",
        on_delete=models.CASCADE
    )
    rider = models.ForeignKey(
        "races.RiderForTeam",
        on_delete=models.CASCADE
    )
    position = models.IntegerField(
        default=1,
    )

    class Meta:
        ordering = ("position", )


class StageScoreForRider(models.Model):
    """
    Model to store the results per rider per stage. Useful for recalculating and aggregating
    """
    stage = models.ForeignKey(
        "races.StageDay",
        on_delete=models.PROTECT,
        related_name="scores_for_riders",
        verbose_name=_("Etappe")
    )
    rider = models.ForeignKey(
        "races.RiderForTeam",
        on_delete=models.PROTECT,
        related_name="scores_for_stages",
        verbose_name=_("Renner")
    )
    position = models.IntegerField(verbose_name=_("Positie"))
    score = models.IntegerField(verbose_name=_("Score"))

    class Meta:
        verbose_name = _("Score voor renner")
        verbose_name_plural = _("Score voor renners")
        ordering = ("stage__round", "stage", "position")

    def __str__(self):
        return _("%(score)d punt(en) voor etappe %(stage)d voor renner %(rider)s") % {
            "score": self.score,
            "stage": self.stage.number,
            "rider": self.rider
        }


class StageScoreForParticipantTeam(models.Model):
    """
    Store all `games.StageScores` for a `games.ParticipantTeam` per stage.
    This should make it easier to see progress per stage per team
    """
    participant_team = models.ForeignKey(
        "games.ParticipantTeam",
        on_delete=models.PROTECT,
        related_name="scores_for_stages",
        verbose_name=_("Team voor deelnemer")
    )
    stage = models.ForeignKey(
        "races.StageDay",
        on_delete=models.PROTECT,
        related_name="scores_for_participants",
        verbose_name=_("Etappe")
    )
    rider_stage_scores = models.ManyToManyField(
        "games.StageScoreForRider",
        blank=True
    )
    score_for_stage = models.IntegerField(
        verbose_name=_("Totaal voor etappe"),
        default=0
    )
    accumulated_score = models.IntegerField(
        verbose_name=_("Geaccumuleerde score"),
        default=0
    )

    class Meta:
        verbose_name = _("Etappe score voor team")
        verbose_name_plural = _("Etappe scores voor teams")
        constraints = [
            models.UniqueConstraint(fields=["participant_team", "stage"], name="unique score for participant and stage")
        ]
        ordering = ("stage__round", "stage")

    def __str__(self):
        return _("Etappe scores voor %(team)s") % {
            "team": self.participant_team.user.get_full_name()
        }

    # @property
    # def score_for_stage(self):
    #     return self.rider_stage_scores.aggregate(total=Sum("score"))["total"]
    #
    # @property
    # def accumulated_score(self):
    #     return StageScoreForParticipantTeam.objects.filter(
    #         participant_team=self.participant_team,
    #         stage__date__lte=self.stage.date
    #     ).aggregate(total=Sum("rider_stage_scores__score"))["total"]
