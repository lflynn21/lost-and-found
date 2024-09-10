from django.test import TestCase
from django.contrib.auth.models import User
from googlemap.models import Location


class LocationModelTest(TestCase):
    def setUp(self):
        # Create a test user and a test location
        self.location = Location.objects.create(latitude=38.0359, longitude=-78.5037)

    def test_location_attributes(self):
        # Check that the location has the correct attributes
        self.assertEqual(self.location.latitude, 38.0359)
        self.assertEqual(self.location.longitude, -78.5037)

    def test_location_methods(self):
        # Check that the location has the correct methods
        self.assertEqual(self.location.__str__(), "38.0359, -78.5037")