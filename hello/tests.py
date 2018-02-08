# Django test cases
# Author: Christopher Besser
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from .views import index
class SimpleTest(TestCase):
    # Set up for tests
    # Param: self - the test suite
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    # Run the test
    # Param: self - the test suite
    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        request.user = AnonymousUser()
        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        self.assertEqual(response.status_code, 200)