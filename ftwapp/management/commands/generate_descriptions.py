# ftwapp/management/commands/generate_descriptions.py

from django.core.management.base import BaseCommand
from ftwapp.models import Word
from openai import OpenAI
from django.conf import settings
from django.db.models import Q

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class Command(BaseCommand):
    help = "Generate Dutch descriptions for new words using GPT"

    def handle(self, *args, **kwargs):
        words = Word.objects.filter(Q(description__isnull=True) | Q(description=""))

        for word in words:
            prompt = f"Schrijf een korte, duidelijke beschrijving in het Nederlands voor het woord '{word.name}'. Gebruik eenvoudige taal."

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Je bent een behulpzame assistent die korte en duidelijke beschrijvingen maakt in het Nederlands, eenvoudig te begrijpen voor iedereen."},
                    {"role": "user", "content": prompt}
                ]
            )

            description = response.choices[0].message.content.strip()
            word.description = description
            word.save()
            self.stdout.write(self.style.SUCCESS(f"Beschrijving toegevoegd voor: {word.name}"))

