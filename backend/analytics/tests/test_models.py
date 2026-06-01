import pytest

"""
pytest-django automatically creates a test db for as aliased as test_our_db_name
"""
@pytest.mark.django_db
def test_smoke_setup():
    """Confirm pytest has access to the testing db"""
    assert True


import pytest
from analytics.tests.factories import StoreFactory, ProductFactory, OrderLineFactory
from analytics.models import Store, Product, OrderLine

@pytest.mark.django_db
def test_store_creation():
    store = StoreFactory(name="Mi Tienda de Test", category="Fashion")
    
    assert Store.objects.count() == 1
    assert store.name == "Mi Tienda de Test"
    assert store.category == "Fashion"
    assert str(store) == "Mi Tienda de Test"

@pytest.mark.django_db
def test_product_linked_to_store():
    product = ProductFactory(name="Teclado Mecánico")
    
    assert Product.objects.count() == 1
    assert Store.objects.count() == 1
    assert product.store.products.first() == product
    assert str(product) == "Teclado Mecánico"

@pytest.mark.django_db
def test_order_line_captures_historical_price():
    product = ProductFactory(price=99.99)
    order_line = OrderLineFactory(product=product, quantity=2)
    
    assert OrderLine.objects.count() == 1
    assert order_line.price_at_purchase == 99.99
    assert str(order_line) == f"2x {product.name}"