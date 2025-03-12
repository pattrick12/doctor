# patients/management/commands/dbshell_docker.py

from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Open MySQL shell using Docker'

    def handle(self, *args, **options):
        container_name = 'doctor_db'
        mysql_user = 'root'
        mysql_password = 'doctor456'
        command = f'docker exec -it {container_name} mysql -u {mysql_user} -p{mysql_password}'
        subprocess.call(command, shell=True)