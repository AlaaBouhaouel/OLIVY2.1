from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.index, name='index'),
    path('video_feed_page/', views.video_feed_page, name='video_feed_page'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('import_image', views.detection_image, name='import_image'),
    path('weather/<str:lat>/<str:lng>/<str:email>', views.weather_view, name='weather_with_coords'),
    path('map', views.map_view, name='map_view'),
    path('weather/', views.weather_view, name='weather'),
    path('Olivy_chat/', views.Olivy_chat, name='Olivy_chat'),
    path('from_drone/', views.from_drone, name='from_drone'),





]
#

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
