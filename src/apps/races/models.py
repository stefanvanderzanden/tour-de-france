from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django_countries.fields import CountryField
from polymorphic.models import PolymorphicModel


class Round(models.Model):
    ROUND_TYPE_CHOICES = (
        ("tour-de-france", _("Tour de France")),
        ("giro-d-italia", _("Giro d'Italia")),
        ("vuelta-a-espana", _("Vuelta a España")),
    )
    start_date = models.DateField(verbose_name=_("Startdatum"))
    # start_time = models.TimeField(verbose_name=_("Starttijd"))
    end_date = models.DateField(verbose_name=_("Einddatum"))
    year = models.PositiveSmallIntegerField(verbose_name=_("Year"))
    type = models.CharField(
        max_length=15,
        verbose_name=_("Type"),
        choices=ROUND_TYPE_CHOICES,
    )

    class Meta:
        verbose_name = _("Ronde")
        verbose_name_plural = _("Rondes")

    def __str__(self):
        return f"{self.get_type_display()} {self.start_date.year}"

    @property
    def has_started(self):
        return timezone.now().date() > self.start_date


class Rider(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_("Voornaam"))
    last_name = models.CharField(max_length=100, verbose_name=_("Achternaam"))
    birth_date = models.DateField(verbose_name=_("Geboortedatum"))
    country = CountryField()


    class Meta:
        verbose_name = _("Renner")
        verbose_name_plural = _("Renners")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



class RiderForTeam(models.Model):
    RIDER_QUALITY_CHOICES = (
        (1, _("Weinig")),
        (2, _("Gemiddeld")),
        (3, _("Veel")),
    )
    team_leader = models.BooleanField(default=False, verbose_name=_("Kopman"))
    number = models.IntegerField(verbose_name=_("Rugnummer"))
    team = models.ForeignKey("races.TeamForRound", on_delete=models.CASCADE, verbose_name=_("Team voor ronde"))
    rider = models.ForeignKey("races.Rider", on_delete=models.CASCADE, verbose_name=_("Renner"))
    sprint_quality = models.IntegerField(
        choices=RIDER_QUALITY_CHOICES,
        verbose_name=_("Sprint kwaliteit"),
        null=True,
        blank=True,
    )
    climb_quality = models.IntegerField(
        choices=RIDER_QUALITY_CHOICES,
        verbose_name=_("Klim kwaliteit"),
        null=True,
        blank=True,
    )
    attack_quality = models.IntegerField(
        choices=RIDER_QUALITY_CHOICES,
        verbose_name=_("Aanval kwaliteit"),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Renner nog in koers"),
        default=True
    )
    photo = models.ImageField(
        verbose_name=_("Photo"),
        upload_to="profile_pictures",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Renner voor team")
        verbose_name_plural = _("Renners voor team")
        constraints = [
            models.UniqueConstraint(fields=['team', 'rider'], name='unique rider for team')
        ]

    def __str__(self):
        return _("%(rider_number)s - %(rider_first_name)s %(rider_last_name)s") % {
            "rider_number": self.number,
            "rider_first_name": self.rider.first_name,
            "rider_last_name": self.rider.last_name,
        }

    @property
    def full_name(self):
        return self.rider.full_name

    def save(self, *args, **kwargs):
        team_leaders = RiderForTeam.objects.filter(team=self.team, team_leader=True)
        if self.id:
            team_leaders = team_leaders.exclude(id=self.id)
        # Make sure only one teamleader per team is possible
        if (
                self.team_leader and
                team_leaders.count() > 0
        ):
            raise ValidationError(_("Er mag maar 1 kopman per team bestaan"))

        super(RiderForTeam, self).save(*args, **kwargs)


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Naam"))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Team actief")
    )

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return f"{self.name}"


class TeamForRound(models.Model):
    team = models.ForeignKey(
        "races.Team",
        on_delete=models.PROTECT,
        verbose_name=_("Team"),
        help_text=_("Geef hier het team op"),
        limit_choices_to={"is_active": True}
    )
    round = models.ForeignKey(
        "races.Round",
        on_delete=models.PROTECT,
        verbose_name=_("Ronde"),
        help_text=_("Geef hier de ronde op")
    )
    riders = models.ManyToManyField("races.Rider", through="races.RiderForTeam")
    order = models.IntegerField(
        verbose_name=_("Order"),
        default=1,
    )

    class Meta:
        verbose_name = _("Team voor ronde")
        verbose_name_plural = _("Teams voor ronde")
        ordering = ['order']

    def __str__(self):
        return f"Team '{self.team.name}' voor ronde '{self.round}'"


class Day(PolymorphicModel):
    round = models.ForeignKey(
        "races.Round",
        related_name="stages",
        on_delete=models.PROTECT,
        verbose_name=_("Ronde")
    )
    date = models.DateField(
        verbose_name=_("Datum"),
    )

    class Meta:
        verbose_name = _("Ronde dag")
        verbose_name_plural = _("Ronde dagen")
        ordering = ("round", "date")

    def __str__(self):
        return f"Ronde dag: {self.date.strftime('%d-%m-%Y')}"


class RestDay(Day):
    number = models.IntegerField(verbose_name=_("Rustdagnummer"))

    class Meta:
        verbose_name = _("Rustdag")
        verbose_name_plural = _("Rustdagen")

    def __str__(self):
        return f"Rustdag {self.number}"


class StageDay(Day):
    TYPE_CHOICES = (
        ("mountain", _("Bergen")),
        ("individual-time-trial", _("Individuele tijdrit")),
        ("team-time-trial", _("Ploegen tijdrit")),
        ("hilly", _("Heuvelachtig")),
        ("flat", _("Plat")),
    )
    number = models.IntegerField(verbose_name=_("Etappe nummer"))
    start_city = models.CharField(max_length=100, verbose_name=_("Start stad"))
    end_city = models.CharField(max_length=100, verbose_name=_("Eind stad"))
    distance = models.DecimalField(
        verbose_name=_("Afstand"),
        max_length=7,
        max_digits=4,
        decimal_places=1)
    stage_type = models.CharField(verbose_name=_("Etappe type"), max_length=32, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = _("Etappe")
        verbose_name_plural = _("Etappes")
        ordering = ("round", "number")

    def __str__(self):
        return _("Etappe %(number)d (%(round)s)") % {
            "number": self.number,
            "round": self.round
        }


class StageResult(models.Model):
    stage = models.ForeignKey(
        "races.StageDay",
        on_delete=models.PROTECT,
        verbose_name=_("Etappe")
    )
    rider = models.ForeignKey(
        "races.RiderForTeam",
        on_delete=models.PROTECT,
        verbose_name=_("Renner")
    )
    position = models.IntegerField(verbose_name=_("Positie"))

    class Meta:
        verbose_name = _("Etappe resultaat")
        verbose_name_plural = _("Etappe resultaten")
        ordering = ("stage__round", "stage")
