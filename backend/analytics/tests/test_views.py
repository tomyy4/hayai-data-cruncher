from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_hello_world(client):
    response = client.get(reverse("hello_world"))
    result = response.json()
    assert result.get("message") == "Hello world"

