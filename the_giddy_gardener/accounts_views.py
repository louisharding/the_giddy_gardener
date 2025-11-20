from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse


def login_or_signup(request):
    """Combined login + signup view. Renders both forms and handles POSTs.

    POST contains either `login_submit` or `signup_submit` to disambiguate.
    On successful signup we auto-login the new user.
    """
    next_url = request.POST.get('next') or request.GET.get('next') or reverse('growing_projects:home')

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            signup_form = UserCreationForm()
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect(next_url)
        elif 'signup_submit' in request.POST:
            signup_form = UserCreationForm(request.POST)
            login_form = AuthenticationForm()
            if signup_form.is_valid():
                user = signup_form.save()
                auth_login(request, user)
                return redirect(next_url)
        else:
            login_form = AuthenticationForm(request, data=request.POST)
            signup_form = UserCreationForm(request.POST)
    else:
        login_form = AuthenticationForm()
        signup_form = UserCreationForm()

    return render(request, 'account/login.html', {
        'login_form': login_form,
        'signup_form': signup_form,
        'next': next_url,
    })
