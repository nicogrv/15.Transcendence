
import os
from api.models.playerModel import Player
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist and generates a token for them"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--email', help="Admin's email")
        parser.add_argument('--password', help="Admin's password")
        parser.add_argument('--no-input', help="Read options from the environment", action='store_true')

    def handle(self, *args, **options):
        if options['no_input']:
            options['username'] = os.environ['DJANGO_SUPERUSER_USERNAME']
            options['email'] = os.environ['DJANGO_SUPERUSER_EMAIL']
            options['password'] = os.environ['DJANGO_SUPERUSER_PASSWORD']

        if not Player.objects.filter(username=options['username']).exists():
            Player.objects.create_superuser(username=options['username'], email=options['email'], password=options['password'])
            self.stdout.write(self.style.SUCCESS(f"Superuser {options['username']} created."))

        user = Player.objects.get(username=options['username'])