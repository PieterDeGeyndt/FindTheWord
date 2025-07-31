import nested_admin
from django import forms
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Subcategory, Word
from django.urls import reverse
from django.utils.html import format_html

#-- Nested Admin for Categories and Subcategories --
class WordInline(nested_admin.NestedTabularInline):
    model = Word
    extra = 0
    fields = ('id_display', 'name', 'subcategory', 'category', 'description')
    readonly_fields = ('id_display',)
 
    def id_display(self, obj):
        return obj.id
    id_display.short_description = "ID"

class SubcategoryInline(nested_admin.NestedStackedInline):
    model = Subcategory
    inlines = [WordInline]
    extra = 0
    fields = ('id_display', 'name', 'category', 'image')
    readonly_fields = ('id_display',)

    def id_display(self, obj):
        return obj.id
    id_display.short_description = "ID"

class CategoryAdmin(nested_admin.NestedModelAdmin):
    inlines = [SubcategoryInline]
    list_display = ('id', 'name')
    readonly_fields = ('id_display',)
    fields = ('id_display', 'name', 'parent', 'image')

    def id_display(self, obj):
        return obj.id
    id_display.short_description = "ID"

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
class CategoryAdmin(nested_admin.NestedModelAdmin, ImportExportModelAdmin):
    form = CategoryAdminForm
    resource_class = CategoryResource

    inlines = [SubcategoryInline]
    list_display = ('id','name',)

    readonly_fields = ('image_preview',)
    fields = ('image_preview', 'name', 'parent', 'image', 'image_search')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "(No image)"
    image_preview.short_description = "Image Preview"

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )



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
    resource_class = SubcategoryResource
    list_display = ('id', 'name', 'category')
    
    readonly_fields = ('image_preview',)
    fields = ('image_preview', 'name', 'category', 'image', 'image_search')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "(No image)"
    image_preview.short_description = "Image Preview"

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )


# -------- Word --------
class WordResource(resources.ModelResource):
    class Meta:
        model = Word
        fields = '__all__'

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
    list_display = ('id', 'name', 'category', 'subcategory', 'has_image', 'has_description')
    list_filter = ('category', 'subcategory')
    search_fields = ('name',)
    
    readonly_fields = ('image_preview',)
    fields = ('image_preview', 'image', 'image_search','name', 'category', 'subcategory', 'description')

    change_form_template = "admin/ftwapp/word/change_form.html"

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Image"

    def has_description(self, obj):
        return bool(obj.description)
    has_description.boolean = True
    has_description.short_description = "Description"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "(No image)"
    image_preview.short_description = "Image Preview"

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        if object_id:
            words = list(Word.objects.order_by('id').values_list('id', flat=True))
            try:
                current_index = words.index(int(object_id))
            except ValueError:
                current_index = -1

            if current_index != -1:
                if current_index > 0:
                    prev_id = words[current_index - 1]
                    prev_word_url = reverse("admin:ftwapp_word_change", args=[prev_id])
                    extra_context['prev_word_url'] = prev_word_url

                if current_index < len(words) - 1:
                    next_id = words[current_index + 1]
                    next_word_url = reverse("admin:ftwapp_word_change", args=[next_id])
                    extra_context['next_word_url'] = next_word_url

        return super().changeform_view(request, object_id, form_url, extra_context)

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'ftwapp/image_search.js',
        )
