from csv import reader

from django.core.management.base import BaseCommand, CommandError
from backend.settings import GROUP_FILES_DIR
from core.models import Group


class Command(BaseCommand):
    """Команда для импорта группы в базу данных"""

    help = 'Import group  data from CSV into the bd'

    def handle(self, *args, **kwargs):
        try:
            with open(
                GROUP_FILES_DIR,
                encoding='UTF-8'
            ) as group:
                Group.objects.bulk_create([
                    Group(
                        name=row[0]
                    )
                    for row in reader(group)
                ])
        except:
            raise CommandError('group not import')
