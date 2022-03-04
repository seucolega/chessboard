import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user() -> User:
    return User.objects.create(username='user', password='secret')


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
