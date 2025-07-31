from django.core.management.base import BaseCommand
from ftwapp.models import Word, Category, Subcategory
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings

class Command(BaseCommand):
    help = "Generate and save images for Words, Categories, and Subcategories using SerpAPI"

    def fetch_image_url(self, search_query):
        self.stdout.write(f"Searching image for: {search_query}")
        params = {
            "engine": "google_images",
            "q": search_query,
            "api_key": settings.SERPAPI_KEY,
            "num": 1
        }
        try:
            response = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "images_results" in data and data["images_results"]:
                return data["images_results"][0]["original"]
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching image for {search_query}: {e}"))
        return None

    def save_image_from_url(self, instance, field_name, image_url):
        try:
            img_temp = NamedTemporaryFile(delete=True)
            img_response = requests.get(image_url, timeout=10)
            img_response.raise_for_status()
            img_temp.write(img_response.content)
            img_temp.flush()

            file_name = f"{instance.name.replace(' ', '_')}.jpg"
            getattr(instance, field_name).save(file_name, File(img_temp), save=True)
            img_temp.close()
            self.stdout.write(self.style.SUCCESS(f"Image saved for {instance.name}"))
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to download image for {instance.name}: {e}"))

    def handle(self, *args, **kwargs):
        # Handle Words
        words = Word.objects.filter(image__isnull=True) | Word.objects.filter(image="")
        for word in words.distinct():
            if word.image:
                self.stdout.write(self.style.NOTICE(f"Skipping word '{word.name}': image already exists"))
                continue
            url = self.fetch_image_url(word.name)
            if url:
                self.save_image_from_url(word, 'image', url)
            else:
                self.stdout.write(self.style.WARNING(f"No image found for word '{word.name}'"))

        # Handle Categories
        categories = Category.objects.filter(image__isnull=True) | Category.objects.filter(image="")
        for category in categories.distinct():
            if category.image:
                self.stdout.write(self.style.NOTICE(f"Skipping category '{category.name}': image already exists"))
                continue
            url = self.fetch_image_url(category.name)
            if url:
                self.save_image_from_url(category, 'image', url)
            else:
                self.stdout.write(self.style.WARNING(f"No image found for category '{category.name}'"))

        # Handle Subcategories
        subcategories = Subcategory.objects.filter(image__isnull=True) | Subcategory.objects.filter(image="")
        for subcat in subcategories.distinct():
            if subcat.image:
                self.stdout.write(self.style.NOTICE(f"Skipping subcategory '{subcat.name}': image already exists"))
                continue
            url = self.fetch_image_url(subcat.name)
            if url:
                self.save_image_from_url(subcat, 'image', url)
            else:
                self.stdout.write(self.style.WARNING(f"No image found for subcategory '{subcat.name}'"))
