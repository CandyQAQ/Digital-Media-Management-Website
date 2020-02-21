from django.urls import path

from . import views
app_name = 'mymusic'
urlpatterns = [
    path('get_crawl', views.get_crawl),
    path('get_soft_music', views.get_soft_music),
    path('get_noisy_music', views.get_noisy_music),
    path('get_crawl_music', views.get_crawl_music),
    path('get_soft_image', views.get_soft_image),
    path('get_noisy_image', views.get_noisy_image),
    path('get_crawl_image', views.get_crawl_image),
    path('get_soft_txt', views.get_soft_txt),
    path('get_noisy_txt', views.get_noisy_txt),
    path('get_crawl_txt', views.get_crawl_txt),
    path('upload_image1', views.upload_image1),
    path('upload_image2', views.upload_image2),
    path('add_watermark', views.add_watermark),
    path('upload_image', views.upload_image),
    path('upload_others', views.upload_others),
    path('detect_similarity', views.detect_similarity)
]