from urllib import response
from django.test import Client, TestCase
from .models import Passenger,Flight,Airport
# Create your tests here.


class FLightTestCase(TestCase):

    def setUp(self):
         
        #create Airport
        a1=Airport.objects.create(code="ABC",city="NewYork")
        a2=Airport.objects.create(code="DEF",city="London")

        #Create Flights

        Flight.objects.create(origin=a1,destination=a2,duration=200)
        Flight.objects.create(origin=a1,destination=a1,duration=200)
        Flight.objects.create(origin=a1,destination=a2,duration=-200)

    def test_departure_count(self):
        a = Airport.objects.get(code="ABC")
        self.assertEqual(a.departures.count(),3)

    def test_arrival_count(self):
        a = Airport.objects.get(code="DEF")
        self.assertEqual(a.arrivals.count(),2)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="ABC")
        a2 = Airport.objects.get(code="DEF")
        f=Flight.objects.first(origin=a1,destination=a2)

        c=Client()
        response=c.get(f"/flights/{f.id}")
        self.assertEquals(response.status_code,200)
        a1 = Airport.objects.get(code="ABC")
        f=Flight.objects.create(origin=a1,destination=a1,duration=100)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="ABC")
        a2= Airport.objects.get(code="DEF")
        f=Flight.objects.create(origin=a1,destination=a2,duration=-100)
        self.assertFalse(f.is_valid_flight())
    
    def test_index(self):
        c=Client()
        response=c.get("/flight/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flights'].count(),3)


