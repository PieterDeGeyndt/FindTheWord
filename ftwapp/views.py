import os
import requests
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from tempfile import NamedTemporaryFile
from django.core.files import File
from .models import Category, Subcategory, Word
from django.conf import settings

@staff_member_required
def download_and_assign_image(request):
    image_url = request.GET.get('url')
    obj_id = request.GET.get('id')
    model_type = request.GET.get('type')

    if not image_url or not obj_id or not model_type:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    if model_type == 'category':
        from .models import Category as Model
    elif model_type == 'subcategory':
        from .models import Subcategory as Model
    elif model_type == 'word':
        from .models import Word as Model
    else:
        return JsonResponse({'error': 'Invalid type'}, status=400)

    obj = Model.objects.get(pk=obj_id)

    img_temp = NamedTemporaryFile(delete=True)
    resp = requests.get(image_url)
    if resp.status_code != 200:
        return JsonResponse({'error': 'Image download failed'}, status=500)
    img_temp.write(resp.content)
    img_temp.flush()

    filename = os.path.basename(image_url.split("?")[0])[:50]
    obj.image.save(filename, File(img_temp))
    obj.save()

    return JsonResponse({'success': True})


@staff_member_required
def image_search_view(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    api_key = settings.SERPAPI_KEY  # ⬅️ Use the SerpAPI key from settings
    serp_url = f'https://serpapi.com/search?q={query}&tbm=isch&ijn=0&api_key={api_key}'

    resp = requests.get(serp_url)
    if resp.status_code == 200:
        data = resp.json()
        return JsonResponse({'images': data.get('images_results', [])})
    else:
        return JsonResponse({'error': 'Failed to fetch images'}, status=500)

def home(request):
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'home.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()

    # Get words directly under this category
    direct_words = Word.objects.filter(category=category)

    # Get words from subcategories
    subcategory_words = Word.objects.filter(subcategory__in=subcategories)

    # Combine them
    words = direct_words | subcategory_words
    words = words.distinct()

    return render(request, 'category_detail.html', {
        'category': category,
        'subcategories': subcategories,
        'words': words,
    })

def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    words = subcategory.words.all()
    return render(request, 'subcategory_detail.html', {
        'subcategory': subcategory,
        'words': words,
    })

def word_detail(request, pk):
    word = get_object_or_404(Word, pk=pk)
    return render(request, 'word_detail.html', {'word': word})

def info(request):
    return render(request, 'info.html')