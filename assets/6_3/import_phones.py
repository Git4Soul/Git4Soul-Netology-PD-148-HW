import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='phones.csv', help='CSV file path')

    def handle(self, *args, **options):
        file_path = options['file']
        with open(file_path, 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

            for row in phones:
                phone, created = Phone.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'price': float(row['price']),
                        'image': row['image'],
                        'release_date': row['release_date'],
                        'lte_exists': row['lte_exists'].lower() == 'true',
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Добавлен: {phone.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Обновлён: {phone.name}'))