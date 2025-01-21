from django.test import TestCase

from system.models import RepairLog, User, Vehicle


# Create your tests here.

class RepairLogTestCase(TestCase):


    def test_create_repairlog(self):
        customer_user = User.objects.get()
        vehicle = Vehicle.objects.get()
        print(customer_user)
        repairlog = RepairLog.objects.create(
            malfunctionType="ER1",
            customer=customer_user,
            vehicle=vehicle,
            description="Motor issue reported.",
            fixed=True,
            repairDate='2024-10-17T10:30:00'
        )
        print(repairlog.malfunctionId)

    def test_something(self):
        vehicle_id = 1
        repairlog = RepairLog.objects.filter(vehivle__id__exect=vehicle_id)