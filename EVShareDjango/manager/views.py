from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,reverse
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from system.models import Location, Vehicle, RepairLog, User, RentLog, Payment
from . import forms

# Create your views here.

@login_required()
@require_http_methods(['GET'])
def show_reports(request):
    locations = Location.objects.filter(
        isAvailable=True)
    location_list = [
        {
            "id": loc.id,
            "name": loc.locationName,
            "address": loc.locationAddress,
            "latitude": loc.locationLat,
            "longitude": loc.locationLong,
            "VehicleCount": loc.vehicle_set.count(),
            "EBikeCount": Vehicle.objects.filter(lastLocation=loc, vehicleType="EBike").count(),
            "EScooterCount": Vehicle.objects.filter(lastLocation=loc, vehicleType="EScooter").count(),
        } for loc in locations
    ]
    return render(request, 'charts.html', {'locations': location_list})


def money_earned_per_location(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    rentlogs = RentLog.objects.all()

    if start_date:
        rentlogs = rentlogs.filter(endDate__gte=parse_date(start_date))
    if end_date:
        rentlogs = rentlogs.filter(endDate__lte=parse_date(end_date))

    data = (
        rentlogs.values('returnLocation__locationName')
        .annotate(total_earned=Sum('price'))
        .order_by('-total_earned')
    )

    response_data = [
        {'location': item['returnLocation__locationName'], 'total_earned': item['total_earned']}
         for item in data if item['returnLocation__locationName']!=None
    ]
    return JsonResponse(response_data, safe=False)


def cars_per_location(request):
    data = (
        Vehicle.objects
        .values("lastLocation__locationName")
        .annotate(total_cars=Count("id"))
        .order_by("-total_cars")
    )
    result = [{"location": entry["lastLocation__locationName"], "total_cars": entry["total_cars"]} for entry in data]
    return JsonResponse(result, safe=False)

def most_reported_broken_cars(request):
    data = (
        RepairLog.objects
        .values("vehicle__id")
        .annotate(report_count=Count("id"))
        .order_by("-report_count")
    )
    result = [{"vehicle_id": entry["vehicle__id"], "report_count": entry["report_count"]} for entry in data]
    return JsonResponse(result, safe=False)


def most_used_rental_location(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    rentals = RentLog.objects.all()

    if start_date:
        rentals = rentals.filter(startDate__gte=parse_date(start_date))
    if end_date:
        rentals = rentals.filter(startDate__lte=parse_date(end_date))

    data = (
        rentals.values('returnLocation__locationName')
        .annotate(rental_count=Count('id'))
        .order_by('-rental_count')
    )

    response_data = [{'location': item['returnLocation__locationName'], 'rental_count': item['rental_count']} for item
                     in data]
    return JsonResponse(response_data, safe=False)

def most_rented_vehicle_types(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    rentals = RentLog.objects.all()

    if start_date:
        rentals = rentals.filter(startDate__gte=parse_date(start_date))
    if end_date:
        rentals = rentals.filter(startDate__lte=parse_date(end_date))

    data = (
        rentals.values('vehicle__vehicleType')
        .annotate(rental_count=Count('id'))
        .order_by('-rental_count')
    )

    response_data = [{'vehicle_type': item['vehicle__vehicleType'], 'rental_count': item['rental_count']} for item in
                     data]
    return JsonResponse(response_data, safe=False)



