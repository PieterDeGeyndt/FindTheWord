
from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child_categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Word(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='words/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='words', null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='words', null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        if not self.subcategory and not self.category:
            raise ValidationError('Kies minstens een subcategorie of categorie.')
        if self.subcategory and self.category:
            raise ValidationError('Kies niet zowel een subcategorie als een categorie.')