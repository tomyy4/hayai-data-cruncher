import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
import random
from analytics.models import Store, Product, OrderLine


from faker import Faker
import faker_commerce

fake = Faker()
fake.add_provider(faker_commerce.Provider)

class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.Faker('company')
    category = factory.Iterator(['Electronics', 'Fashion', 'Home', 'Beauty', 'Sports'])


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    store = factory.SubFactory(StoreFactory) # Create a store if not provided
    name = factory.LazyFunction(fake.ecommerce_name)
    sku = factory.Sequence(lambda n: f"SKU-{n:06d}-{random.randint(100, 999)}")
    price = factory.LazyAttribute(lambda o: round(random.uniform(5.99, 499.99), 2))

    @classmethod
    def _setup_next_sequence(cls):
        return 1


class OrderLineFactory(DjangoModelFactory):
    class Meta:
        model = OrderLine

    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyAttribute(lambda o: random.randint(1, 5))
    price_at_purchase = factory.SelfAttribute('product.price') # Copies the price of the product automatically
    purchased_at = factory.Faker('date_time_between', start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())