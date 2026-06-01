import pytest

"""
pytest-django automatically creates a test db for as aliased as test_our_db_name
"""
@pytest.mark.django_db
def test_smoke_setup():
    """Confirm pytest has access to the testing db"""
    assert True