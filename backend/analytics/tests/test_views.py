import pytest

from django.urls import reverse
from django.core.cache import cache
from rest_framework.test import APIClient
from analytics.tests.factories import OrderLineFactory, StoreFactory
from analytics.events import OrderEventDispatcher


@pytest.mark.django_db
def test_hello_world(client):
    response = client.get(reverse("hello_world"))
    result = response.json()
    assert result.get("message") == "Hello world"


@pytest.mark.django_db
def test_dashboard_analytics_cache_and_event_invalidation():
    client = APIClient()
    url = reverse('global-dashboard-analytics')
    
    cache.clear()
    
    store = StoreFactory(id=1)
    OrderLineFactory(product__store=store)

    # 2. First rquerst(Cache Miss): Must go do db
    response_1 = client.get(url)
    assert response_1.status_code == 200
    assert response_1.data['source'] == 'database'
    
    assert cache.get("dashboard_analytics_global") is not None

    # 3. Second request: must be cached
    response_2 = client.get(url)
    assert response_2.status_code == 200
    assert response_2.data['source'] == 'cache'

    OrderEventDispatcher.dispatch_order_created(store_id=str(store.id))

    # 5. Check: Cache must been destroyed
    assert cache.get("dashboard_analytics_global") is None
    assert cache.get(f"dashboard_analytics_{store.id}") is None

    # No existing cache, must recalculate
    response_3 = client.get(url)
    assert response_3.status_code == 200
    assert response_3.data['source'] == 'database'