"""
Used for setting up common methods for API testing
"""

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from enum import Enum, unique


@unique
class APIMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseTestCase(APITestCase):
    def setUp(self) -> None:
        """
        Used for initial setup of Test cases
        """
        super().setUp()
        self.client = APIClient()

    def request(
            self, method: APIMethods, url_name=None, body=None, format="json", url=None
    ):
        """
        Used to make authenticated request for API testing.

        Args:
            method (APIMethods): API method name to be used from APIMethods Enum
            url_name (str_, optional): URL name, which is used for getting the URL in reverse.
            Defaults to None.
            body (dict, optional): Body of the request. Defaults to None.
            format (str, optional): Format of the request body. Defaults to "json".
            url (str, optional): URL of the request except base. Defaults to None.

        Returns:
            response : Response object of the request
        """
        response = None
        if url:
            url = 'http://127.0.0.1:8000/' + url
        else:
            url = reverse(url_name)
        if method == APIMethods.GET:
            response = self.client.get(url, data=body, format=format)
        if method == APIMethods.POST:
            response = self.client.post(url, data=body, format=format)
        if method == APIMethods.PUT:
            response = self.client.put(url, data=body, format=format)
        if method == APIMethods.PATCH:
            response = self.client.patch(url, data=body, format=format)
        if method == APIMethods.DELETE:
            response = self.client.delete(url, data=body, format=format)
        return response
