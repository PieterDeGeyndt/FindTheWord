from django import forms
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html
import os
import requests
from django.shortcuts import render
from django.conf import settings
from .models import Category, Subcategory, Word

# -------- Category --------
class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
    
    image_search = forms.CharField(
        required=False,
        label="Zoek afbeelding",
        help_text="Type hier een zoekterm en klik op 'Search Images'."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    change_form_template = "admin/ftwapp/change_form.html"

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<pk>/search-images/', self.admin_site.admin_view(self.search_images), name='category_search_images'),
        ]
        return custom_urls + urls

    def search_images(self, request, pk):
        obj = self.get_object(request, pk)

        query = obj.name  # use category or word name as search text
        api_key = os.getenv("SERPAPI_KEY")  # Ensure you have set this in your environment variables
        serp_url = f'https://serpapi.com/search.json?q={query}&tbm=isch&ijn=0&api_key={api_key}'

        resp = requests.get(serp_url)
        images = []
        if resp.status_code == 200:
            data = resp.json()
            images = data.get('images_results', [])

        context = {
            'opts': self.model._meta,
            'original': obj,
            'images': images,
            'title': f"Afbeeldingen zoeken voor: {obj.name}",
        }
        return render(request, 'admin/ftwapp/image_search_results.html', context)

# -------- Subcategory --------
class SubcategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'
        
    image_search = forms.CharField(
        required=False,
        label="Zoek afbeelding",
       help_text="Type hier een zoekterm en klik op 'Search Images'."
   )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    form = SubcategoryAdminForm
    change_form_template = "admin/ftwapp/change_form.html"

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<pk>/search-images/', self.admin_site.admin_view(self.search_images), name='subcategory_search_images'),
        ]
        return custom_urls + urls

    def search_images(self, request, pk):
        obj = self.get_object(request, pk)
        if obj:
            self.message_user(request, f"Google image search gestart voor: {obj.name}")
        return redirect(request.META.get('HTTP_REFERER'))

    def render_change_form(self, request, context, *args, **kwargs):
        obj = context.get('original')
        if obj:
            search_url = reverse('admin:subcategory_search_images', args=[obj.pk])
            context['extra_button'] = format_html('<a class="button" href="{}">Zoek afbeeldingen</a>', search_url)
        return super().render_change_form(request, context, *args, **kwargs)


# -------- Word --------
class WordAdminForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = '__all__'
    
    image_search = forms.CharField(
        required=False,
        label="Zoek afbeelding",
       help_text="Type hier een zoekterm en klik op 'Search Images'."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    form = WordAdminForm
    change_form_template = "admin/ftwapp/change_form.html"

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<pk>/search-images/', self.admin_site.admin_view(self.search_images), name='word_search_images'),
        ]
        return custom_urls + urls

    def search_images(self, request, pk):
        obj = self.get_object(request, pk)
        if obj:
            self.message_user(request, f"Google image search gestart voor: {obj.name}")
        return redirect(request.META.get('HTTP_REFERER'))

    def render_change_form(self, request, context, *args, **kwargs):
        obj = context.get('original')
        if obj:
            search_url = reverse('admin:word_search_images', args=[obj.pk])
            context['extra_button'] = format_html('<a class="button" href="{}">Zoek afbeeldingen</a>', search_url)
        return super().render_change_form(request, context, *args, **kwargs)
