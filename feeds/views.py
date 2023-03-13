import requests
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import PersonalInformation
# Create your views here.

def login_view(request):
    print("login_view called")
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    print(form)
    return render(request, 'login.html', {'form': form})

@login_required
def home_page(request):
    personalInfo = PersonalInformation.objects.all()
    about = About.objects.all()
    projects = Project.objects.all()
    skills = Skill.objects.all()
    context = {
        "personalInfo": personalInfo,
        "about": about,
        "projects": projects,
        "skills": skills
    }

    return render(request, 'home_page.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def repositories(request):
    # Get the user's GitHub username from the personal information model
    personal_info = PersonalInformation.objects.first()
    username = personal_info.github.split('/')[-1]

    # Make a request to the GitHub API to get the list of repositories
    response = requests.get(f'https://api.github.com/users/{username}/repos')
    repositories = response.json()

    # Pass the list of repositories to the template
    context = {'repositories': repositories}
    return render(request, 'repositories.html', context)