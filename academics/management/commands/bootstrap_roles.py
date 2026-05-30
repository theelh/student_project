from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crée les groupes et permissions de base pour le projet.'

    def handle(self, *args, **options):
        manager_group, _ = Group.objects.get_or_create(name='Gestionnaire')
        viewer_group, _ = Group.objects.get_or_create(name='Consultation')
        admin_group, _ = Group.objects.get_or_create(name='Administrateur')

        all_academic_permissions = Permission.objects.filter(content_type__app_label='academics')
        view_permissions = all_academic_permissions.filter(codename__startswith='view_')

        manager_group.permissions.set(all_academic_permissions)
        viewer_group.permissions.set(view_permissions)
        admin_group.permissions.set(Permission.objects.all())

        self.stdout.write(self.style.SUCCESS('Groupes et permissions créés/mis à jour avec succès.'))
