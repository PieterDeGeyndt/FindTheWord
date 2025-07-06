from django import forms
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html

from .models import Category, Subcategory, Word

# -------- Category --------
class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    change_form_template = "admin/ftwapp/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<pk>/search-images/', self.admin_site.admin_view(self.search_images), name='category_search_images'),
        ]
        return custom_urls + urls

    def search_images(self, request, pk):
        obj = self.get_object(request, pk)
        if obj:
            # Hier kan je je eigen image search functie aanroepen
            self.message_user(request, f"Google image search gestart voor: {obj.name}")
        return redirect(request.META.get('HTTP_REFERER'))

    def render_change_form(self, request, context, *args, **kwargs):
        obj = context.get('original')
        if obj:
            search_url = reverse('admin:category_search_images', args=[obj.pk])
            context['extra_button'] = format_html('<a class="button" href="{}">Zoek afbeeldingen</a>', search_url)
        return super().render_change_form(request, context, *args, **kwargs)


# -------- Subcategory --------
class SubcategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    form = SubcategoryAdminForm
    change_form_template = "admin/ftwapp/change_form.html"

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    form = WordAdminForm
    change_form_template = "admin/ftwapp/change_form.html"

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
