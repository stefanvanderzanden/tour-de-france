import re
import requests
import datetime
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError

from apps.races.models import Rider, Team, TeamForRound, RiderForTeam, Round

COUNTRY_MAPPING = {
    "pol": "PL",
    "col": "CO",
    "lux": "LU",
    "aus": "AU",
    "lat": "LV",
    "crc": "CR",
    "ita": "IT",
    "rsa": "ZA",
    "usa": "US",
    "nzl": "NZ",
    "esp": "ES",
    "fra": "FR",
    "nor": "NO",
    "por": "PT",
    "ger": "DE",
    "gbr": "GB",
    "ecu": "EC",
    "can": "CA",
    "svk": "SK",
    "aut": "AT",
    "den": "DK",
    "bel": "BE",
    "eri": "ER",
    "sui": "CH",
    "kaz": "KZ",
    "ned": "NL",
    "slo": "SI",
}


class Command(BaseCommand):
    help = "Download all teams and riders from tour website"

    def add_arguments(self, parser):
        parser.add_argument("start_url", type=str)
        # parser.add_argument("base_url", nargs="+", type=str)

    def handle(self, *args, **options):
        regex = r"^.+?[^\/:](?=[?\/]|$)"
        start_url = options.get("start_url")
        match = re.match(regex, start_url)
        base_url = None
        if match:
            base_url = match.group(0)
        if not base_url:
            raise CommandError("Geen base url kunnen vinden")

        page = requests.get(start_url)
        if not page.status_code == 200:
            raise CommandError(f"Site niet kunnen benaderen: {page.status_code}")

        soup = BeautifulSoup(page.content, "html.parser")
        competitors = soup.find_all(class_="list list--competitors")
        if len(competitors) != 1:
            raise CommandError(f"Verwachtte 1 lijst met renners kreeg er {len(competitors)}")

        infixes = ["van", "der", "de"]
        competitors = competitors[0]
        team_for_round = None
        round = Round.objects.get(
            start_date__year=2025,
            type="tour-de-france"
        )
        for competitor_element in competitors.children:
            if competitor_element.name == "h3":
                team_name = competitor_element.get_text()
                team, created = Team.objects.get_or_create(
                    name=team_name,
                    defaults={"is_active": True}
                )
                team_for_round, created = TeamForRound.objects.get_or_create(
                    team=team,
                    round=round
                )

            elif competitor_element.name == "div":
                for index, rider in enumerate(competitor_element.find_all(class_="list__box__item"), start=1):
                    number = rider.find(class_="bib").get_text().strip()
                    rider_link = rider.find(class_="runner__link", href=True)
                    rider_name = rider_link.get_text().strip().lower()
                    print(f"Start aan {rider_name}")
                    rider_url = rider_link["href"]
                    rider_page = requests.get(f"{base_url}{rider_url}")
                    rider_soup = BeautifulSoup(rider_page.content, "html.parser")
                    birth_info = rider_soup.find(class_="riderInfos__birth").get_text().strip()
                    birth_date = birth_info.split("born on ")[1]
                    birth_date_date = datetime.datetime.strptime(birth_date, "%d/%m/%Y")

                    country_info = rider_soup.find(class_="riderInfos__country__name").get_text().strip()
                    name = ' '.join(
                        [word.capitalize() if word not in infixes else word for word in rider_name.split()])
                    first_name = name.split()[0]
                    last_name = " ".join(name.split()[1:])
                    short_code = country_info.replace("(", "").replace(")", "")
                    country_code = COUNTRY_MAPPING.get(short_code)
                    rider, created = Rider.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name,
                        birth_date=birth_date_date,
                        country=country_code
                    )
                    if team_for_round:
                        rider_for_team, created = RiderForTeam.objects.get_or_create(
                            team_leader=True if index == 1 else False,
                            number=number,
                            team=team_for_round,
                            rider=rider,
                            sprint_quality=1,
                            climb_quality=1,
                            attack_quality=1,
                        )
