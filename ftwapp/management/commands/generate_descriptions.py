# ftwapp/management/commands/generate_descriptions.py

from django.core.management.base import BaseCommand
from ftwapp.models import Word
from openai import OpenAI
from django.conf import settings
from django.db.models import Q


client = OpenAI(api_key= settings.OPENAI_API_KEY)
language=settings.WEB_LANGUAGE
class Command(BaseCommand):
    help = "Generate descriptions for words using ChatGPT"

    def handle(self, *args, **kwargs):
        words = Word.objects.filter(Q(description__isnull=True) | Q(description=""))
        for word in words:
            prompt = f"Write a short, clear description for the word '{word.name}' in {language}, easy to understand for everyone."
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes clear, short descriptions."},
                    {"role": "user", "content": prompt}
                ]
            )
            description = response.choices[0].message.content.strip()
            word.description = description
            word.save()
            self.stdout.write(self.style.SUCCESS(f"Updated: {word.name}"))
