from rest_framework import status 
import pytest
from django.contrib.auth.models import User
@pytest.fixture
def create_collection(api_client):
    def inner(collection):
        return api_client.post('/store/collections/',collection)
    return inner


@pytest.mark.django_db
class TestCollection:
    def  test_if_user_is_anynomous_return_404(self,create_collection):
        response=create_collection({'title':'okay'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def  test_if_user_is_not_anynomous_return_403(self,create_collection,authenticate_user):
        authenticate_user({})
        response=create_collection({'title':'okay'})
        assert response.status_code == status.HTTP_403_FORBIDDEN


    def  test_if_data_is_invalid_return_400(self,create_collection,authenticate_user):
        authenticate_user(User(is_staff=True))
        response=create_collection({'title':''})
        assert response.data['title'] is not None
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # @pytest.mark.skip
    def  test_if_data_is_valid_return_201(self,create_collection,authenticate_user):
        authenticate_user(User(is_staff=True))
        response=create_collection({'title':'okay'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id']>0

