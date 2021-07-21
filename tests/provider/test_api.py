import json

import pytest
from model_bakery import baker
from mozio.provider.models import Provider

pytestmark = pytest.mark.django_db


class TestProvider:
    base_url = 'http://127.0.0.1:8000'
    provider_data = {
        "name": "Tim",
        "email": "tim@app.com",
        "phone_number": "029838981773",
        "currency": "POUND",
        "language": "English"
    }

    def test_list_providers(self, api_client):
        """
        Test liating of all provider
        """
        baker.make(Provider, _quantity=2)
        url = self.base_url + "/providers/"
        response = api_client().get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2

    def test_create_provider_successfully(self, api_client):
        """
        Test the creation of a provider object
        """
        provider_url = self.base_url + "/providers/"
        response = api_client().post(provider_url, self.provider_data)
        assert response.status_code == 201
        assert response.data['name'] == self.provider_data['name']

    def test_retrieve_provider_successfully(self, api_client):
        """
        Test the getting a provider object
        """
        prov = baker.make(Provider)
        url = self.base_url + f"/providers/{prov.id}/"
        response = api_client().get(url)
        assert response.status_code == 200
        assert response.data['name'] == prov.name

    def test_update_provider_successfully(self, api_client):
        """
        Test the updating a provider object
        """
        prov = baker.make(Provider)
        url = self.base_url + f"/providers/{prov.id}/"
        prov = baker.make(Provider)
        data = {
            "name": "Updated NRB"
        }
        response = api_client().patch(url, data)
        assert response.status_code == 200
        assert response.data['name'] == data['name']

    def test_delete_provider_successfully(self, api_client):
        """
        Test the deleting a provider object
        """
        prov = baker.make(Provider)
        url = self.base_url + f"/providers/{prov.id}/"
        response = api_client().delete(url)
        assert response.status_code == 204
