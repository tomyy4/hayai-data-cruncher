from django.core.management.base import BaseCommand
from django.db import transaction
from analytics.models import Store, Product, OrderLine
from analytics.tests.factories import StoreFactory, ProductFactory, OrderLineFactory
import random

class Command(BaseCommand):
    help = 'Generate fake data for performance testing'

    def add_arguments(self, parser):
        # Allows number of records parametrization
        parser.add_argument(
            '--records',
            type=int,
            default=50000,
            help='Number of order lines to create (By default, 50000)'
        )

    def handle(self, *args, **options):
        total_records = options['records']
        
        self.stdout.write(self.style.WARNING(f'🧹 Cleaning everything before start...'))
        OrderLine.objects.all().delete()
        Product.objects.all().delete()
        Store.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('🚀 Init ..'))

        with transaction.atomic():
            self.stdout.write(' -> Creating stores...')
            stores = [StoreFactory.build() for _ in range(10)]
            Store.objects.bulk_create(stores)
            inserted_stores = list(Store.objects.all())

            self.stdout.write(' -> Creating product catalogs...')
            products = []
            for _ in range(200):
                store = random.choice(inserted_stores)
                products.append(ProductFactory.build(store=store))
            Product.objects.bulk_create(products)
            inserted_products = list(Product.objects.all())

            self.stdout.write(f' -> Generating {total_records} of selling records...')
            
            order_lines = []
            for _ in range(total_records):
                product = random.choice(inserted_products)
                order_lines.append(OrderLineFactory.build(product=product))

                # Group in blocks of 10000 to avoid ram saturation
                if len(order_lines) >= 10000:
                    OrderLine.objects.bulk_create(order_lines)
                    order_lines = [] # clean for the next bulk

            if order_lines:
                OrderLine.objects.bulk_create(order_lines)

        self.stdout.write(self.style.SUCCESS(f'✨ Total success! Db populated with {total_records} records.'))