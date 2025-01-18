# messages_wall/urls.py
from django.urls import path
from . import views

app_name = 'messages_wall'

urlpatterns = [
    # Home and general pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # Message Wall URLs
    path('wall/create/', views.create_message_wall, name='create_wall'),
    path('wall/<str:custom_url>/', views.wall_detail, name='wall_detail'),
    path('wall/<str:custom_url>/edit/', views.wall_edit, name='wall_edit'),
    path('wall/<str:custom_url>/delete/', views.wall_delete, name='wall_delete'),
    
    # Message URLs
    path('message/create/<int:wall_id>/', views.create_message, name='create_message'),
    path('message/<int:pk>/edit/', views.message_edit, name='message_edit'),
    path('message/<int:pk>/delete/', views.message_delete, name='message_delete'),
    
    # Timeline URLs
    path('timeline/', views.timeline_list, name='timeline_list'),
    path('timeline/create/', views.timeline_create, name='timeline_create'),
    path('timeline/<int:pk>/', views.timeline_detail, name='timeline_detail'),

    
    # Special Dates URLs
    path('special-dates/', views.special_dates_list, name='special_dates_list'),
    path('special-dates/create/', views.special_date_create, name='special_date_create'),

    
    # Theme URLs
    path('themes/', views.theme_list, name='theme_list'),
    path('themes/<int:pk>/', views.theme_detail, name='theme_detail'),
    
    # API endpoints for AJAX operations
    path('api/update-message-position/', views.update_message_position, name='update_message_position'),
    path('api/upload-media/', views.upload_media, name='upload_media'),

    
    # Gallery URLs
    path('gallery/', views.public_gallery, name='public_gallery'),
    path('gallery/featured/', views.featured_messages, name='featured_messages'),
    
    # Search and filter
    path('search/', views.search_messages, name='search_messages'),
    path('filter/<str:category>/', views.filter_messages, name='filter_messages'),
]