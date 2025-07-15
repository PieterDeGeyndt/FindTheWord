from django.core.management.base import BaseCommand
from ftwapp.models import Word
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings

class Command(BaseCommand):
    help = "Automatically generate and save images for words using SerpAPI"

    def handle(self, *args, **kwargs):
        words = Word.objects.filter(image="")  # or adjust this filter

        for word in words:
            search_query = word.name
            self.stdout.write(f"Searching image for: {search_query}")

            # SerpAPI call
            params = {
                "engine": "google_images",
                "q": search_query,
                "api_key": settings.SERPAPI_KEY,
                "num": 1
            }
            response = requests.get("https://serpapi.com/search.json", params=params)
            data = response.json()

            if "images_results" in data and len(data["images_results"]) > 0:
                image_url = data["images_results"][0]["original"]
                self.stdout.write(f"Found image: {image_url}")

                # Download image
                img_temp = NamedTemporaryFile()
                img_response = requests.get(image_url, timeout=10)
                img_temp.write(img_response.content)
                img_temp.flush()

                # Save to model
                file_name = f"{word.name.replace(' ', '_')}.jpg"
                word.image.save(file_name, File(img_temp), save=True)
                img_temp.close()

                self.stdout.write(self.style.SUCCESS(f"Image saved for {word.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"No image found for {word.name}"))