import json

import pytest
from model_bakery import baker
from mozio.polygon.models import Polygon
from mozio.provider.models import Provider

pytestmark = pytest.mark.django_db


class TestPolygon:
    base_url = 'http://127.0.0.1:8000'
    polygon_data = {
        "name": "NRB",
        "price": 230,
        "provider": 1,
        "poly": "-98.503358 -29.335668, -98.503086 29.335668, -98.503086 29.335423, -98.503358 29.335423, -98.503358 -29.335668" # noqa
    }

    def test_list_polygons(self, api_client):
        """
        Test liating of all polygons
        """
        baker.make(Polygon, _quantity=2)
        url = self.base_url + "/polygons/"
        response = api_client().get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2

    def test_create_polygon_successfully(self, api_client):
        """
        Test the creation of a polygon object
        """
        url = self.base_url + "/polygons/"
        prov = baker.make(Provider)
        self.polygon_data['provider'] = prov.id
        response = api_client().post(url, self.polygon_data)
        assert response.status_code == 201
        assert response.data['name'] == self.polygon_data['name']

    def test_create_polygon_with_bad_poly_data_fails(self, api_client):
        """
        Test the creation of a polygon object with invalid polygon points fails
        """
        url = self.base_url + "/polygons/"
        prov = baker.make(Provider)
        data = {
            "name": "NRB",
            "price": 930,
            "provider": prov.id,
            "poly": "-98.503358 -29.335668, -98.503086 29.335668, -98.503086 29.335423, -98.503358 29.335423, -98.503358 29.335668" # noqa
        }
        response = api_client().post(url, data)
        assert response.status_code == 400
        assert 'Points of LinearRing do not form a closed linestring.' in response.data['poly']

    def test_create_polygon_with_invalid_provider_fails(self, api_client):
        """
        Test the creation of a polygon object with invalid invalid provider fails
        """
        url = self.base_url + "/polygons/"
        data = {
            "name": "NRB",
            "price": 30,
            "provider": 99999,
            "poly": "-98.503358 -29.335668, -98.503086 29.335668, -98.503086 29.335423, -98.503358 29.335423, -98.503358 29.335668" # noqa
        }
        response = api_client().post(url, data)
        assert response.status_code == 400
        assert 'Please enter a valid provider' in response.data['provider']

    def test_retrieve_polygon_successfully(self, api_client):
        """
        Test the getting a polygon object
        """
        poly = baker.make(Polygon)
        url = self.base_url + f"/polygons/{poly.id}/"
        response = api_client().get(url)
        assert response.status_code == 200
        assert response.data['name'] == poly.name

    def test_update_polygon_successfully(self, api_client):
        """
        Test the updating a polygon object
        """
        poly = baker.make(Polygon)
        url = self.base_url + f"/polygons/{poly.id}/"
        prov = baker.make(Provider)
        data = {
            "name": "Updated NRB",
            "price": 300,
            "provider": prov.id,
            "poly": "-98.503358 -29.335668, -98.503086 29.335668, -98.503086 29.335423, -98.503358 29.335423, -98.503358 -29.335668" # noqa
        }
        response = api_client().patch(url, data)
        assert response.status_code == 200
        assert response.data['name'] == data['name']

    def test_delete_polygon_successfully(self, api_client):
        """
        Test the deleting a polygon object
        """
        poly = baker.make(Polygon)
        url = self.base_url + f"/polygons/{poly.id}/"
        response = api_client().delete(url)
        assert response.status_code == 204

    def test_search_polygon_successfuly(self, api_client):
        """
        Test searching for a polygon using longtude and latitude
        """
        url = self.base_url + "/polygons/"
        prov = baker.make(Provider)
        self.polygon_data['provider'] = prov.id
        response = api_client().post(url, self.polygon_data)
        assert response.status_code == 201
        search_url = url + 'get_locations/?long=-98.503358&lat=-29.335668'
        response = api_client().get(search_url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == self.polygon_data['name']
