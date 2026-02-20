import requests
from django.core.management.base import BaseCommand

from ...models import Place

API_URL = "https://api.artic.edu/api/v1/artworks/search"
LIMIT = 100


class Command(BaseCommand):
    help = "Fetch artworks from API and store them as Places"

    def handle(self, *args, **options):
        url = f"{API_URL}?limit={LIMIT}&page=1"

        while url:
            self.stdout.write(f"Fetching {url}...")
            response = requests.get(url)
            if response.status_code != 200:
                self.stderr.write(f"Error fetching {url}: {response.status_code}")
                break

            data = response.json()
            artworks = data.get("data", [])

            for art in artworks:
                place, created = Place.objects.get_or_create(
                    id=art["id"],
                    defaults={"title": art["title"]}
                )
                if created:
                    self.stdout.write(f"Created place: {place.title}")

            url = data.get("pagination", {}).get("next_url")
            if url:
                self.stdout.write(f"Next page: {url}")
            else:
                self.stdout.write("All pages processed.")