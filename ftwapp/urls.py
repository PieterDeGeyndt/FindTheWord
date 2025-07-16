from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_detail, name='subcategory_detail'),
    path('image-search/', views.image_search_view, name='image_search'),
    path('download-image/', views.download_and_assign_image, name='download_image'),
    path('word/<int:pk>/', views.word_detail, name='word_detail'),
    path('info/', views.info, name='info'),
    path('ajax/live-search-cards/', views.live_search_cards, name='live_search_cards'),
]