import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from where_from.names.models import Country, Name, NameCountryProbability


@pytest.fixture
def api_client():
    return APIClient()


# /names/
@pytest.mark.django_db
class TestNamesEndpoint:
    def test_names_endpoint(self, api_client):
        response = api_client.get('/names/?name=Alex')
        assert response.status_code == 200
        data = response.json()
        assert 'countries' in data

    def test_names_endpoint_missing_parameter(self, api_client):
        response = api_client.get('/names/')
        assert response.status_code == 400
        assert 'error' in response.json()

    def test_names_endpoint_empty_result(self, api_client):
        response = api_client.get('/names/?name=NonExistentName12345')
        assert response.status_code == 404
        assert 'message' in response.json()


# /popular-names/
@pytest.mark.django_db
class TestPopularNamesEndpoint:
    def test_popular_names_success(self, api_client):
        country = Country.objects.create(
            code='US',
            name='United States',
        )

        name = Name.objects.create(name='John', count_of_reguests=3, last_accessed=timezone.now())

        NameCountryProbability.objects.create(name_request=name, country=country, probability=0.029237653286472688)

        response = api_client.get('/popular/?country=US')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5

        expected_data = [{'name': 'John', 'count': 3, 'probability': 0.029237653286472688}]
        assert data == expected_data

    def test_popular_names_missing_parameter(self, api_client):
        response = api_client.get('/popular/')
        assert response.status_code == 400
        assert 'error' in response.json()

    def test_popular_names_invalid_country(self, api_client):
        response = api_client.get('/popular/?country=XX')
        assert response.status_code == 404
        assert 'error' in response.json()


@pytest.mark.django_db
class TestAuthentication:
    def setup_method(self):
        self.register_url = reverse('register')
        self.token_url = reverse('token')
        self.test_user_data = {'username': 'testuser', 'password': 'testpass123'}

    def test_user_registration(self, api_client):
        response = api_client.post(self.register_url, self.test_user_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_token_obtain(self, api_client):
        api_client.post(self.register_url, self.test_user_data, format='json')

        response = api_client.post(self.token_url, self.test_user_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_token_obtain_invalid_credentials(self, api_client):
        api_client.post(self.register_url, self.test_user_data, format='json')

        wrong_credentials = {'username': 'testuser', 'password': 'wrongpass'}

        response = api_client.post(self.token_url, wrong_credentials, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
