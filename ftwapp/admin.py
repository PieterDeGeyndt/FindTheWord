from django import forms
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Subcategory, Word
from django.urls import reverse
from django.utils.html import format_html


# -------- Category --------
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'image',)

class CategoryAdminForm(forms.ModelForm):
    image_search = forms.CharField(
        required=False,
        label="Zoek afbeelding",
        help_text="Type hier een zoekterm en klik op 'Search Images'."
    )

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image_search'].widget.attrs.update({'id': 'id_image_search'})

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    form = CategoryAdminForm

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )

    resource_class = CategoryResource


# -------- Subcategory --------
class SubcategoryResource(resources.ModelResource):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'category', 'image',)

class SubcategoryAdminForm(forms.ModelForm):
    image_search = forms.CharField(
        required=False,
        label="Zoek afbeelding",
        help_text="Type hier een zoekterm en klik op 'Search Images'."
    )

    class Meta:
        model = Subcategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image_search'].widget.attrs.update({'id': 'id_image_search'})

@admin.register(Subcategory)
class SubcategoryAdmin(ImportExportModelAdmin):
    form = SubcategoryAdminForm

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )

    resource_class = SubcategoryResource


# -------- Word --------
class WordResource(resources.ModelResource):
    class Meta:
        model = Word
        fields = ('id', 'name', 'subcategory', 'image',)

class WordAdminForm(forms.ModelForm):
    image_search = forms.CharField(
        required=False,
        label="Zoek afbeelding",
        help_text="Type hier een zoekterm en klik op 'Search Images'."
    )

    class Meta:
        model = Word
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image_search'].widget.attrs.update({'id': 'id_image_search'})

@admin.register(Word)
class WordAdmin(ImportExportModelAdmin):
    form = WordAdminForm
    resource_class = WordResource

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )

    change_form_template = "admin/ftwapp/word/change_form.html"
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        if object_id:
            words = list(Word.objects.order_by('id').values_list('id', flat=True))
            print("All word IDs:", words)
            print("Current object_id:", object_id)

            try:
                current_index = words.index(int(object_id))
            except ValueError:
                current_index = -1
            print("Current index:", current_index)

            if current_index != -1:
                if current_index > 0:
                    prev_id = words[current_index - 1]
                    prev_word_url = reverse("admin:ftwapp_word_change", args=[prev_id])
                    extra_context['prev_word_url'] = prev_word_url
                    print("Prev URL:", prev_word_url)

                if current_index < len(words) - 1:
                    next_id = words[current_index + 1]
                    next_word_url = reverse("admin:ftwapp_word_change", args=[next_id])
                    extra_context['next_word_url'] = next_word_url
                    print("Next URL:", next_word_url)

        print("Extra context keys:", extra_context.keys())
        return super().changeform_view(request, object_id, form_url, extra_context)

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "(No image)"

    image_preview.short_description = "Image Preview"