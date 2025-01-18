from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Message, MessageWall, Theme, Timeline, SpecialDate, MediaAttachment
from .forms import MessageForm, MessageWallForm, TimelineForm, SpecialDateForm
from django.contrib import messages
import json

# Home and General Views
def home(request):
    featured_walls = MessageWall.objects.filter(is_public=True).order_by('-created_at')[:6]
    recent_messages = Message.objects.filter(is_public=True).order_by('-created_at')[:8]
    return render(request, 'messages_wall/home.html', {
        'featured_walls': featured_walls,
        'recent_messages': recent_messages
    })

def about(request):
    return render(request, 'messages_wall/about.html')

# Message Wall Views
@login_required
def create_message_wall(request):
    if request.method == 'POST':
        form = MessageWallForm(request.POST)
        if form.is_valid():
            wall = form.save(commit=False)
            wall.owner = request.user
            wall.save()
            messages.success(request, 'Your message wall has been created!')
            return redirect('messages_wall:wall_detail', custom_url=wall.custom_url)
    else:
        form = MessageWallForm()
    return render(request, 'messages_wall/create_wall.html', {'form': form})

def wall_detail(request, custom_url):
    wall = get_object_or_404(MessageWall, custom_url=custom_url)
    messages_list = Message.objects.filter(
        Q(wall=wall, is_public=True) |
        Q(wall=wall, author=request.user)
    ).order_by('-created_at')
    
    paginator = Paginator(messages_list, 12)
    page = request.GET.get('page')
    wall_messages = paginator.get_page(page)
    
    return render(request, 'messages_wall/wall_detail.html', {
        'wall': wall,
        'messages': wall_messages,
        'form': MessageForm() if request.user.is_authenticated else None
    })

@login_required
def wall_edit(request, custom_url):
    wall = get_object_or_404(MessageWall, custom_url=custom_url, owner=request.user)
    if request.method == 'POST':
        form = MessageWallForm(request.POST, instance=wall)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wall updated successfully!')
            return redirect('messages_wall:wall_detail', custom_url=wall.custom_url)
    else:
        form = MessageWallForm(instance=wall)
    return render(request, 'messages_wall/wall_edit.html', {'form': form, 'wall': wall})

@login_required
def wall_delete(request, custom_url):
    wall = get_object_or_404(MessageWall, custom_url=custom_url, owner=request.user)
    if request.method == 'POST':
        wall.delete()
        messages.success(request, 'Wall deleted successfully!')
        return redirect('messages_wall:home')
    return render(request, 'messages_wall/wall_delete.html', {'wall': wall})

# Message Views
@login_required
def create_message(request, wall_id):
    wall = get_object_or_404(MessageWall, id=wall_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.wall = wall
            message.save()
            
            # Handle multiple file uploads
            files = request.FILES.getlist('media_files')
            for file in files:
                MediaAttachment.objects.create(
                    message=message,
                    file=file,
                    type=get_file_type(file.name)
                )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('messages_wall:wall_detail', custom_url=wall.custom_url)
    else:
        form = MessageForm()
    return render(request, 'messages_wall/create_message.html', {'form': form, 'wall': wall})

def get_file_type(filename):
    extension = filename.lower().split('.')[-1]
    if extension in ['jpg', 'jpeg', 'png']:
        return 'image'
    elif extension == 'gif':
        return 'gif'
    elif extension in ['mp3', 'wav']:
        return 'audio'
    return 'other'

@login_required
def message_edit(request, pk):
    message = get_object_or_404(Message, pk=pk, author=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message updated successfully!')
            return redirect('messages_wall:wall_detail', custom_url=message.wall.custom_url)
    else:
        form = MessageForm(instance=message)
    return render(request, 'messages_wall/message_edit.html', {'form': form, 'message': message})

@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk, author=request.user)
    wall_url = message.wall.custom_url
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully!')
        return redirect('messages_wall:wall_detail', custom_url=wall_url)
    return render(request, 'messages_wall/message_delete.html', {'message': message})

# Timeline Views
@login_required
def timeline_list(request):
    timelines = Timeline.objects.filter(user=request.user).order_by('-date')
    return render(request, 'messages_wall/timeline_list.html', {'timelines': timelines})

@login_required
def timeline_create(request):
    if request.method == 'POST':
        form = TimelineForm(request.POST, request.FILES)
        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.user = request.user
            timeline.save()
            messages.success(request, 'Memory added successfully!')
            return redirect('messages_wall:timeline_list')
    else:
        form = TimelineForm()
    return render(request, 'messages_wall/timeline_create.html', {'form': form})

@login_required
def timeline_detail(request, pk):
    timeline = get_object_or_404(Timeline, pk=pk, user=request.user)
    return render(request, 'messages_wall/timeline_detail.html', {'timeline': timeline})

# Special Dates Views
@login_required
def special_dates_list(request):
    dates = SpecialDate.objects.filter(user=request.user).order_by('date')
    return render(request, 'messages_wall/special_dates_list.html', {'dates': dates})

@login_required
def special_date_create(request):
    if request.method == 'POST':
        form = SpecialDateForm(request.POST)
        if form.is_valid():
            date = form.save(commit=False)
            date.user = request.user
            date.save()
            messages.success(request, 'Special date added successfully!')
            return redirect('messages_wall:special_dates_list')
    else:
        form = SpecialDateForm()
    return render(request, 'messages_wall/special_date_create.html', {'form': form})

# Theme Views
def theme_list(request):
    themes = Theme.objects.all()
    return render(request, 'messages_wall/theme_list.html', {'themes': themes})

def theme_detail(request, pk):
    theme = get_object_or_404(Theme, pk=pk)
    return render(request, 'messages_wall/theme_detail.html', {'theme': theme})

# API Views
@login_required
def update_message_position(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_id = data.get('message_id')
        new_position = data.get('position')
        
        message = get_object_or_404(Message, id=message_id)
        if message.author != request.user:
            return HttpResponseForbidden()
            
        message.position = new_position
        message.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def upload_media(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        media = MediaAttachment.objects.create(
            file=file,
            type=get_file_type(file.name)
        )
        return JsonResponse({
            'status': 'success',
            'file_url': media.file.url
        })
    return JsonResponse({'status': 'error'}, status=400)

# Gallery Views
def public_gallery(request):
    messages_list = Message.objects.filter(is_public=True).order_by('-created_at')
    paginator = Paginator(messages_list, 12)
    page = request.GET.get('page')
    messages = paginator.get_page(page)
    return render(request, 'messages_wall/gallery.html', {'messages': messages})

def featured_messages(request):
    featured = Message.objects.filter(is_public=True, is_featured=True).order_by('-created_at')
    return render(request, 'messages_wall/featured.html', {'messages': featured})

# Search and Filter Views
def search_messages(request):
    query = request.GET.get('q', '')
    messages_list = Message.objects.filter(
        Q(content__icontains=query) |
        Q(author__username__icontains=query),
        is_public=True
    ).order_by('-created_at')
    
    paginator = Paginator(messages_list, 12)
    page = request.GET.get('page')
    messages = paginator.get_page(page)
    
    return render(request, 'messages_wall/search_results.html', {
        'messages': messages,
        'query': query
    })

def filter_messages(request, category):
    messages_list = Message.objects.filter(
        category=category,
        is_public=True
    ).order_by('-created_at')
    
    paginator = Paginator(messages_list, 12)
    page = request.GET.get('page')
    messages = paginator.get_page(page)
    
    return render(request, 'messages_wall/filtered_messages.html', {
        'messages': messages,
        'category': category
    })

# Utility Functions
def get_file_type(filename):
    extension = filename.lower().split('.')[-1]
    if extension in ['jpg', 'jpeg', 'png']:
        return 'image'
    elif extension == 'gif':
        return 'gif'
    elif extension in ['mp3', 'wav']:
        return 'audio'
    return 'other'