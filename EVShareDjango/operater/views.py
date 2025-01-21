import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from system.models import Location, Vehicle, RepairLog, User, RentLog, Payment
from . import forms


# Create your views here.

@login_required()
@require_http_methods(['GET', 'POST'])
def add_location(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        location_list = [
            {
                "id": loc.id,
                "name": loc.locationName,
                "address": loc.locationAddress,
                "latitude": loc.locationLat,
                "longitude": loc.locationLong,
                "VehicleCount": loc.vehicle_set.count(),
            } for loc in locations
        ]
        return render(request, 'add_location.html', {'locations': location_list})
    else:
        form = forms.LocationForm(request.POST)
        if form.is_valid():
            locationName = form.cleaned_data['locationName']
            locationAddress = form.cleaned_data['locationAddress']
            latitude = form.cleaned_data['locationLat']
            longitude = form.cleaned_data['locationLong']
            Location.objects.create(locationName=locationName, locationAddress=locationAddress,
                                    locationLat=latitude, locationLong=longitude)
            print(f"locationName:{locationName},locationAddress:{locationAddress},"
                  f"Latitude: {latitude}, Longitude: {longitude}")
            return redirect(reverse('operater:show_location'))
        else:
            return render(request, 'add_location.html', {'form': form})

@login_required()
@require_http_methods(['GET'])
def show_locations(request):
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
    return render(request, 'show_location.html', {'locations': location_list})


@login_required()
@require_http_methods(['POST'])
def update_location(request):
    location_id = request.POST.get('location_id')
    new_location_name = request.POST.get('newLocationName')
    new_location_address = request.POST.get('newLocationAddress')
    Location.objects.filter(id=location_id).update(locationName=new_location_name,locationAddress=new_location_address)
    return redirect(reverse('operater:show_location'))



@login_required()
@require_http_methods(['GET'])
def delete_location(request, location_id):
    location = Location.objects.get(id=location_id)
    location.isAvailable = False
    location.save()
    return redirect(reverse('operater:show_location'))


@login_required()
@require_http_methods(['GET'])
def add_vehicle(request):
    if request.method == 'GET':
        LocationId = request.GET.get('locationId')
        location = Location.objects.get(id=LocationId)
        vehicleType = request.GET.get('vehicleType')
        if not location:
            return HttpResponse("Cannot find location")
        Vehicle.objects.create(lastLocation=location, vehicleType=vehicleType)
        return redirect(reverse('operater:show_location'))

@login_required()
@require_http_methods(['GET'])
def show_vehicle(request):
    if request.method == 'GET':
        orderby = request.GET.get('order', '').strip()
        repair = request.GET.get('repair', '').strip()
        parked = request.GET.get('parked', '').strip()
        LocationId = request.GET.get('locationId')
        location = Location.objects.get(id=LocationId)
        if not location:
            return HttpResponse("Cannot find location")
        vehicles = location.vehicle_set.all()
        if orderby:
            vehicles = vehicles.order_by(orderby)
        if repair:
            vehicles = vehicles.filter(needsRepair=True)
        if parked:
            vehicles = vehicles.filter(isParked=True)
        vehicle_list = [
            {
                "id": vehicle.id,
                "charge": vehicle.charge,
                "needsRepair": vehicle.needsRepair,
                "isParked": vehicle.isParked,
                "vehicleLat": vehicle.vehicleLat,
                "vehicleLong": vehicle.vehicleLong,
                "vehicleType":vehicle.vehicleType
            } for vehicle in vehicles
        ]
        return render(request, "show_vehicle.html", {'vehicles': vehicle_list,
                                                     'locationId': LocationId,'locationName':location.locationName})

@login_required()
@require_http_methods(["GET", "POST"])
def button_function(request, ButtonName):
    if request.method == 'GET':
        if ButtonName == "repair":
            vehicle_id = request.GET.get('vehicleId')
            try:
                repair_log = RepairLog.objects.filter(vehicle__id=vehicle_id).first()
                if not repair_log:
                    return JsonResponse({'error': 'No repair log found for this vehicle'}, status=404)
                if repair_log.fixed is True:
                    return JsonResponse({'message': 'This vehicle has been repaired.'}, status=400)
                if repair_log:
                    return JsonResponse({
                        'malfunctionType': repair_log.malfunctionType,
                        'reportDate': repair_log.reportDate,
                        'customerId': repair_log.customer.id,
                        'vehicleId': repair_log.vehicle.id,
                        'description': repair_log.description,
                        'operator': repair_log.operator.id if repair_log.operator else None,
                        'Fixed': repair_log.fixed,
                        'repairDate': repair_log.repairDate
                    })
                else:
                    return JsonResponse({'error': 'No repair log found for this vehicle'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        elif ButtonName == "move":
            vehicle_id = request.GET.get('vehicleId')
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
                location_id = vehicle.lastLocation.id
                location_name = vehicle.lastLocation.locationName
                location_list = list(Location.objects.filter(isAvailable=True).values('id', 'locationName'))

                return JsonResponse({
                    'locationId': location_id,
                    'locationName': location_name,
                    'locationList': location_list,
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    elif ButtonName == "RENT LOG":
        return redirect(reverse('operater:show_rent_logs'))
    else:
        if ButtonName == "charge":
            charge_value = request.POST.get('charge')
            vehicleId = request.POST.get('vehicleID')
            locationId = request.POST.get('locationId')
            Vehicle.objects.filter(id=vehicleId).update(
                charge=charge_value
            )
            return redirect(reverse('operater:show_vehicle') + f'?locationId={locationId}')
        elif ButtonName == "repair":
            locationId = request.POST.get('locationId')
            malfunction_type = request.POST.get('malfunctionType')
            vehicle_id = request.POST.get('vehicle')
            description = request.POST.get('description')
            operator_id = request.POST.get('operator')
            operator = User.objects.get(id=operator_id) if operator_id else None
            fixed = request.POST.get('Fixed') == 'on'
            repair_date = request.POST.get('repairDate')

            try:
                repair_log = RepairLog.objects.get(vehicle__id=vehicle_id)

                repair_log.malfunctionType = malfunction_type
                repair_log.description = description
                repair_log.operator = operator
                repair_log.fixed = fixed
                repair_log.repairDate = repair_date
                repair_log.save()
                Vehicle.objects.filter(id=vehicle_id).update(needsRepair=False,isParked=True)
                if locationId:
                    return redirect(reverse('operater:show_vehicle') + f'?locationId={locationId}')
                else:
                    return redirect(reverse('operater:show_repairlogs'))
            except RepairLog.DoesNotExist:
                return JsonResponse({'error': 'No repair log found for this vehicle ID.'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        elif ButtonName == "move":
            past_location_id = request.POST.get('currentLocationId')
            vehicle_id = request.POST.get('vehicleId')
            new_location_id = request.POST.get('move_to')
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.lastLocation = Location.objects.get(id=new_location_id)
            vehicle.save()
            return redirect(reverse('operater:show_vehicle') + f'?locationId={past_location_id}')


def addtestdata(request):
    rentlog = RentLog.objects.get(id=6)
    rentlog.returnLocation = Location.objects.get(id=4)
    rentlog.save()


@login_required()
@require_http_methods(['GET'])
def show_rent_logs(request):
    customer_username = request.GET.get('customer', '').strip()
    vehicle_id = request.GET.get('vehicle', '').strip()

    rent_logs = RentLog.objects.all()

    if customer_username:
        rent_logs = rent_logs.filter(customer__username__exact=customer_username)

    if vehicle_id:
        rent_logs = rent_logs.filter(vehicle__id=vehicle_id)

    rent_log_list = [
        {
            'id': rent_log.id,
            'vehicle': rent_log.vehicle.id,
            'customer': rent_log.customer.username if rent_log.customer else "N/A",
            'startDate': rent_log.startDate,
            'endDate': rent_log.endDate if rent_log.endDate else "Not returned yet",
            'pickupLocation': rent_log.vehicle.lastLocation.locationName if rent_log.vehicle.lastLocation else "N/A",
            'returnLocation': rent_log.returnLocation.locationName if rent_log.returnLocation else "N/A",
        } for rent_log in rent_logs
    ]

    # 渲染模板并传递租车日志列表
    return render(request, 'show_rent_logs.html', {'rent_logs': rent_log_list, 'customer_username': customer_username, 'vehicle_id': vehicle_id})

@login_required
@require_http_methods(['GET'])
def show_payment(request):
    # Get search parameters from the query string
    customer_username = request.GET.get('customer', '').strip()
    id = request.GET.get('id', '').strip()

    # Retrieve all Payment entries, using select_related to optimize queries
    payment_logs = Payment.objects.select_related('customer').all()  # Initialize here

    # Filter by customer username if provided
    if customer_username:
        payment_logs = payment_logs.filter(customer__username__iexact=customer_username)
    if id:
        payment_logs = payment_logs.filter(customer__id__iexact=id)

    # Construct the list of payment logs
    payment_log_list = [
        {
            'id': payment_log.customer.id if payment_log.customer else "N/A",
            'customer': payment_log.customer.username if payment_log.customer else "N/A",
            'amount': payment_log.amount,
            'paymentDate': payment_log.paymentDate,
            'remark': payment_log.remark,
        } for payment_log in payment_logs
    ]

    # Render the template and pass the payment log list and search parameters
    return render(request, 'show_payment.html', {'payment_logs': payment_log_list, 'customer_username': customer_username, 'id': id})

@login_required()
@require_http_methods(['GET'])
def show_repairlogs(request):
    customer_username = request.GET.get('customer', '').strip()
    vehicle_id = request.GET.get('vehicle', '').strip()


    repair_logs = RepairLog.objects.all().order_by('fixed', 'id')

    if customer_username:
        repair_logs = repair_logs.filter(customer__username__exact=customer_username)

    if vehicle_id:
        repair_logs = repair_logs.filter(vehicle__id=vehicle_id)

    repairlog_list = [
        {
            'id': repair_log.id,
            'vehicle': repair_log.vehicle.id,
            'customer': repair_log.customer.username if repair_log.customer else "N/A",
            'reportDate': repair_log.reportDate,
            'repairDate': repair_log.repairDate if repair_log.repairDate else "Not fixed yet",
            'description': repair_log.description,
            'fixed': repair_log.fixed,
            'operator':repair_log.operator.id if repair_log.operator else "N/A",
        } for repair_log in repair_logs
    ]

    return render(request, 'show_repairlog.html', {'repair_logs': repairlog_list, 'customer_username': customer_username, 'vehicle_id': vehicle_id})