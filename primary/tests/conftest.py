import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate_user(api_client):
   def inner(user):
    return api_client.force_authenticate(user=user)
   return inner