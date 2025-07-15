from django import forms
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Subcategory, Word

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

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )

    resource_class = WordResource
