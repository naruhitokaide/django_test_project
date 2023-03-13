import pytest
import json
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from feeds.models import PersonalInformation
from unittest.mock import patch

@pytest.fixture
def client():
    client = Client()
    return client

@pytest.fixture
def test_user():
    user = User.objects.create_user(username='testuser', password='password')
    return user

@pytest.mark.django_db
def test_login_view(client, test_user):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'form' in response.context

    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
    assert response.status_code == 302   # should redirect to home page

@pytest.mark.django_db
def test_home_page(client, test_user):
    client.login(username='testuser', password='password')
    response = client.get(reverse('home_page'))
    assert response.status_code == 200
    assert 'personalInfo' in response.context
    assert 'about' in response.context
    assert 'projects' in response.context
    assert 'skills' in response.context

@pytest.mark.django_db
def test_logout_view(client, test_user):
    client.login(username='testuser', password='password')
    response = client.get(reverse('logout'))
    assert response.status_code == 302   # should redirect to login page

@pytest.mark.django_db
def test_redirect_unregistered_path_middleware(client):
    response = client.get('/unregistered-path/')
    assert response.status_code == 302   # should redirect to login page

    response = client.get(reverse('login'))
    assert response.status_code == 200

    response = client.get('/')
    assert response.status_code == 302   # should redirect to login page
    
@pytest.fixture
def mock_github_response():
    with open('mock_github_response.json') as f:
        return json.load(f)


@pytest.fixture
def personal_info():
    return PersonalInformation.objects.create(
        name_complete='Test User',
        avatar='images/avatar.jpg',
        mini_about='A brief introduction',
        email='test@example.com',
        cv='cv/resume.pdf',
        github='https://github.com/test',
        linkedin='https://www.linkedin.com/in/test/'
    )


@pytest.mark.django_db
@patch('feeds.views.requests.get')
def test_repositories_view(mock_get, test_user, client, personal_info, mock_github_response):
    mock_get.return_value.json.return_value = mock_github_response
    
    url = reverse('repositories')
    client.force_login(test_user)
    response = client.get(url)
    
    assert response.status_code == 200
    assert len(response.context['repositories']) == 2
    assert response.context['repositories'][0]['name'] == 'test-repo1'
    assert response.context['repositories'][1]['name'] == 'test-repo2'
    assert 'repositories.html' in [t.name for t in response.templates]
    assert 'repositories' in response.context
    
    repositories = response.context['repositories']
    assert repositories == mock_github_response