from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm, UserSettingsForm
from messages_wall.models import MessageWall, Message, Timeline, SpecialDate

@login_required
def profile_view(request):
    walls = MessageWall.objects.filter(owner=request.user).order_by('-created_at')
    received_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')[:5]
    sent_messages = Message.objects.filter(author=request.user).order_by('-created_at')[:5]
    special_dates = SpecialDate.objects.filter(user=request.user).order_by('date')[:5]
    
    return render(request, 'users/profile.html', {
        'walls': walls,
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'special_dates': special_dates
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def dashboard(request):
    walls_count = MessageWall.objects.filter(owner=request.user).count()
    messages_count = Message.objects.filter(author=request.user).count()
    received_messages_count = Message.objects.filter(recipient=request.user).count()
    timeline_count = Timeline.objects.filter(user=request.user).count()
    
    recent_activity = Message.objects.filter(
        recipient=request.user
    ).order_by('-created_at')[:10]
    
    return render(request, 'users/dashboard.html', {
        'walls_count': walls_count,
        'messages_count': messages_count,
        'received_messages_count': received_messages_count,
        'timeline_count': timeline_count,
        'recent_activity': recent_activity
    })

@login_required
def user_settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('users:settings')
    else:
        form = UserSettingsForm(instance=request.user)
    return render(request, 'users/settings.html', {'form': form})