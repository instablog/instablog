from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.forms import SignupForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup Successfully.')
            next_url = request.GET.get('next', 'blog:index')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'form.html', {
        'form': form,
    })


@login_required
def profile_detail(request):
    profile, is_created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile_detail.html', {
        'profile': profile,
    })


@login_required
def profile_edit(request):
    profile, is_created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully.')
            next_url = request.GET.get('next', 'accounts.views.profile_detail')
            return redirect(next_url)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'form.html', {
        'form': form,
    })

