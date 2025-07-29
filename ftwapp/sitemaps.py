from django.contrib.sitemaps import Sitemap
from .models import Category, Subcategory, Word

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f"/category/{obj.pk}/"

class SubcategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Subcategory.objects.all()

    def location(self, obj):
        return f"/subcategory/{obj.pk}/"

class WordSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Word.objects.all()

    def location(self, obj):
        return f"/word/{obj.pk}/"