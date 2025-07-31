import os
import requests
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from tempfile import NamedTemporaryFile
from django.core.files import File
from .models import Category, Subcategory, Word
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse

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

#-----------------------------Global Search view ----------------------------------------------------

from django.urls import reverse

def live_search_cards(request):
    query = request.GET.get('q', '')

    categories = []
    subcategories = []
    words = []

    if query:
        categories = Category.objects.filter(name__icontains=query)
        subcategories = Subcategory.objects.filter(name__icontains=query)
        words = Word.objects.filter(name__icontains=query)

    results = {
        'categories': [
            {
                'id': c.id,
                'name': c.name,
                'image': c.image.url if c.image else '',
                'url': reverse('category_detail', args=[c.id]),
            } for c in categories
        ],
        'subcategories': [
            {
                'id': s.id,
                'name': s.name,
                'image': s.image.url if s.image else '',
                'url': reverse('subcategory_detail', args=[s.id]),
            } for s in subcategories
        ],
        'words': [
            {
                'id': w.id,
                'name': w.name,
                'image': w.image.url if w.image else '',
                'url': reverse('word_detail', args=[w.id]),
            } for w in words
        ]
    }

    return JsonResponse(results)

#-----------------------------Home view ----------------------------------------------------


def home(request):
    order = request.GET.get('order')
    if order:
        request.session['order'] = order
    else:
        order = request.session.get('order', 'alphabetical')

    categories = Category.objects.filter(parent__isnull=True)

    if order == 'last_used':
        categories = categories.order_by('-last_used')
    else:
        categories = categories.order_by('name')

    return render(request, 'home.html', {
        'categories': categories,
        'order': order,
    })

#-----------------------------Category detail view ----------------------------------------------------

def category_detail(request, category_id):
    order = request.GET.get('order')
    if order:
        request.session['order'] = order
    else:
        order = request.session.get('order', 'alphabetical')

    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()

    if order == 'last_used':
        subcategories = subcategories.order_by('-last_used')
    else:
        subcategories = subcategories.order_by('name')

    direct_words = Word.objects.filter(category=category)
    subcategory_words = Word.objects.filter(subcategory__in=subcategories)
    words = direct_words | subcategory_words
    words = words.distinct()

    if order == 'last_used':
        words = words.order_by('-last_used')
    else:
        words = words.order_by('name')

    return render(request, 'category_detail.html', {
        'category': category,
        'subcategories': subcategories,
        'words': words,
        'order': order,
    })

#-----------------------------Subcategory detail view ----------------------------------------------------

def subcategory_detail(request, subcategory_id):
    order = request.GET.get('order')
    if order:
        request.session['order'] = order
    else:
        order = request.session.get('order', 'alphabetical')

    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    words = subcategory.words.all()

    if order == 'last_used':
        words = words.order_by('-last_used')
    else:
        if subcategory.name == "De Maanden":
            months_order = [
                "Januari", "Februari", "Maart", "April", "Mei", "Juni",
                "Juli", "Augustus", "September", "Oktober", "November", "December"
            ]
            words = sorted(words, key=lambda w: months_order.index(w.name) if w.name in months_order else 999)
        else:
            if subcategory.name == "De Seizoenen":
                seasons_order = [
                    "Lente", "Zomer", "Herfst", "Winter"
                ]
                words = sorted(words, key=lambda w: seasons_order.index(w.name) if w.name in seasons_order else 999)
            else:
                if subcategory.name == "Dagen":
                    days_order = [
                        "Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"
                    ]
                    words = sorted(words, key=lambda w: days_order.index(w.name) if w.name in days_order else 999)
                else:    
                    words = words.order_by('name')    

    return render(request, 'subcategory_detail.html', {
        'subcategory': subcategory,
        'words': words,
        'order': order,
    })

#-----------------------------Word detail view ----------------------------------------------------

from django.utils import timezone

def word_detail(request, pk):
    word = get_object_or_404(Word, pk=pk)
    now = timezone.now()

    # Update word
    word.last_used = now
    word.save(update_fields=['last_used'])

    # Update subcategory
    if word.subcategory:
        word.subcategory.last_used = now
        word.subcategory.save(update_fields=['last_used'])

        # Update category via subcategory
        if word.subcategory.category:
            word.subcategory.category.last_used = now
            word.subcategory.category.save(update_fields=['last_used'])

    # If word directly belongs to a category
    elif word.category:
        word.category.last_used = now
        word.category.save(update_fields=['last_used'])

    # Get current ordering preference from session
    order = request.session.get('order', 'alphabetical')

    return render(request, 'word_detail.html', {'word': word, 'order': order})

#-----------------------------Info view ----------------------------------------------------

def info(request):
    return render(request, 'info.html')

#-----------------------------Info view ----------------------------------------------------

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "",
        "Sitemap: https://zoekhetwoord.be/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")