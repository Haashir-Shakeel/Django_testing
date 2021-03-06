from ast import Pass
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Flight,Passenger

# Create your views here.
def index(request):
    return render(request, "Flight/index.html",{
        "flights":Flight.objects.all(),
    }
    )

def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "Flight/flight.html",{
        "flight": flight,
        "passengers": flight.passengers.all() , #this .passengers is related_name
        "non_passengers": Passenger.objects.exclude(flights=flight) #pasensgers excludig those in this flight
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse("flight",args =(flight.id,)))