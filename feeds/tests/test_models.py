import pytest
from feeds.models import PersonalInformation, About, Project, Contact, Skill


@pytest.mark.django_db
def test_personal_information_model():
    PersonalInformation.objects.create(
        name_complete='Test User',
        avatar='images/avatar.jpg',
        mini_about='A brief introduction',
        email='test@example.com',
        cv='cv/resume.pdf',
        github='https://github.com/test',
        linkedin='https://www.linkedin.com/in/test/'
    )
    assert PersonalInformation.objects.count() == 1


@pytest.mark.django_db
def test_about_model():
    About.objects.create(
        title='About Me',
        description1='First paragraph of about me',
        description2='Second paragraph of about me',
        about_avatar='images/about_avatar.jpg'
    )
    assert About.objects.count() == 1


@pytest.mark.django_db
def test_project_model():
    Project.objects.create(
        title='Project A',
        skill='Python, Django, PostgreSQL',
        link='https://github.com/test/project-a',
        image='images/project_a.jpg'
    )
    assert Project.objects.count() == 1


@pytest.mark.django_db
def test_contact_model():
    Contact.objects.create(
        title='Contact Me',
        email='test@example.com',
        location='New York City',
        msg='Hello, I am interested in working with you!',
        link='https://example.com',
        image='images/contact.jpg',
        github='https://github.com/test',
        linkedin='https://www.linkedin.com/in/test/'
    )
    assert Contact.objects.count() == 1


@pytest.mark.django_db
def test_skill_model():
    Skill.objects.create(
        name='Python',
        percentage=90
    )
    assert Skill.objects.count() == 1