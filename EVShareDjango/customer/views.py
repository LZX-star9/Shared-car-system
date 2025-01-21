import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from system.models import Location, Vehicle, RentLog, RepairLog, User


# Create your views here.

@login_required()
@require_http_methods(['GET', 'POST'])
def index(request):
    locations = Location.objects.all()
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
    if request.user.is_authenticated:
        user = request.user
        rentlogs = RentLog.objects.filter(customer=user, endDate__isnull=True)
        rentlog_list = [
            {
                "vehicleId": rentlog.vehicle.id,
                "vehicleType":rentlog.vehicle.vehicleType,
                "energy": rentlog.vehicle.charge,
                "startDate": rentlog.startDate.isoformat(),
                "starttime":rentlog.startDate.strftime('%Y-%m-%d %H:%M:%S'),
                "rent_id": rentlog.id
            } for rentlog in rentlogs
        ]
        return render(request, 'customer_index.html', {"locations": location_list,
                                                       "rentlogs": rentlog_list
                                                       })
    else:
        return render(request, 'customer_index.html', {'locations': location_list})


@login_required()
@require_http_methods(['GET', 'POST'])
def rent_vehicle(request):
    if request.method == 'GET':
        LocationId = request.GET.get('locationId')
        location = Location.objects.get(id=LocationId)
        if not location:
            return HttpResponse("Cannot find location")
        vehicles = location.vehicle_set.all()
        vehicle_list = [
            {
                "id": vehicle.id,
                "charge": vehicle.charge,
                "needsRepair": vehicle.needsRepair,
                "isParked": vehicle.isParked,
                "vehicleType":vehicle.vehicleType,
            } for vehicle in vehicles
        ]
        return render(request, "rent_vehicle.html", {'vehicles': vehicle_list,
                                                     'locationId': LocationId})
    else:
        user = request.user
        if user.balance < 0:
            messages.error(request, "Your balance is insufficient, please recharge it as soon as possible.")
            return redirect(reverse('customer:index'))
        vehicle_id = request.POST.get('vehicleId')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        vehicle.isParked = False
        vehicle.save()
        RentLog.objects.create(customer=request.user, vehicle=vehicle)
        return redirect(reverse('customer:index'))

@login_required()
@require_http_methods(['GET','POST'])
def return_vehicle(request):
    if request.method == 'GET':
        vehicle_id = request.GET.get('vehicleId')
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            location_id = vehicle.lastLocation.id
            location_name = vehicle.lastLocation.locationName
            location_list = list(Location.objects.all().values('id', 'locationName'))

            return JsonResponse({
                'locationId': location_id,
                'locationName': location_name,
                'locationList': location_list,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        vehicle_id = request.POST.get('vehicleId')
        return_location_id = request.POST.get('move_to')
        energy = request.POST.get('energy')
        user = request.user
        location = Location.objects.get(id=return_location_id)

        vehicle = Vehicle.objects.get(id=vehicle_id)
        vehicle.isParked = True
        vehicle.charge = energy
        vehicle.lastLocation = location
        vehicle.save()
        rentlog = RentLog.objects.filter(customer=user, vehicle=vehicle,endDate__isnull=True).first()
        rentlog.endDate = timezone.now()
        location = Location.objects.get(id=return_location_id)
        rentlog.returnLocation = location

        if user.cardType==2 and user.cardExpiry >= timezone.now().date():
            should_pay = 0
            messages.add_message(
                request,
                messages.INFO,
                "You are a noble Super Plus user, this use is free!")
        elif user.cardType==1 and user.cardExpiry >= timezone.now().date() and vehicle.vehicleType in ["EBike","EScooter"]:
            should_pay = 0
            messages.add_message(
                request,
                messages.INFO,
                "You are a noble Plus user, this use is free!")
        else:
            should_pay = (rentlog.endDate - rentlog.startDate).total_seconds() // 60 * 0.02
            messages.add_message(
                request,
                messages.INFO,
                f"The trip costs £{should_pay} and your balance is £{(user.balance - should_pay):.2f}")
        user.balance = user.balance - should_pay
        user.save()
        rentlog.price = should_pay
        rentlog.save()
        if user.balance> 0:
            return redirect(reverse('customer:index'))
        else:
            messages.error(request, "Your balance is insufficient, please recharge it as soon as possible, otherwise you can't rent it next time")
            return redirect(reverse('customer:index'))


@login_required()
@require_http_methods(['POST'])
def report_problem(request):
    malfunction_type = request.POST.get('malfunctionType')
    vehicle_id = request.POST.get('vehicle')
    description = request.POST.get('description')
    try:
        RepairLog.objects.create(
            vehicle=Vehicle.objects.get(id=vehicle_id),
            customer=request.user,
            description=description,
            malfunctionType=malfunction_type,
        )
        rent_log = RentLog.objects.get(vehicle__id=vehicle_id,endDate__isnull=True)
        rent_log.endDate = timezone.now()
        rent_log.save()
        Vehicle.objects.filter(id=vehicle_id).update(needsRepair=True)
        messages.success(request,
                         "We have received the problem report. We will process it quickly. The order has been cancelled for you.")
        return redirect(reverse('customer:index'))
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
