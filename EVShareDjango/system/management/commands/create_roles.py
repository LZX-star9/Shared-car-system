from django.core.management.base import BaseCommand
from system.models import User

class Command(BaseCommand):
    help = 'Create Operator or Manager user'

    def add_arguments(self, parser):
        parser.add_argument(
            'role',
            type=str,
            help='Specify the role to create: "operator" or "manager"',
            choices=['operator', 'manager']
        )

    def handle(self, *args, **options):
        role = options['role']

        if role == 'operator':
            self.create_operator()
        elif role == 'manager':
            self.create_manager()
        else:
            self.stdout.write(self.style.ERROR("Invalid role specified"))

    def create_operator(self):
        username = input("Enter username for operator: ")
        password = input("Enter password for operator: ")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
            return

        operator = User(
            username=username,
            password=password,
            userType="OP",
            isActive=True
        )
        operator.save()
        self.stdout.write(self.style.SUCCESS(f"Operator '{username}' created successfully."))

    def create_manager(self):
        username = input("Enter username for manager: ")
        password = input("Enter password for manager: ")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
            return

        manager = User(
            username=username,
            password=password,
            userType="MN",
            isActive=True
        )
        manager.save()
        self.stdout.write(self.style.SUCCESS(f"Manager '{username}' created successfully."))
