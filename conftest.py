import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from properties.models.property import Property


def make_user(name, role="owner", **extra):
    User = get_user_model()
    return User.objects.create_user(
        username=name,
        email=f"{name}@example.com",
        password="testpass123",
        role=role,
        **extra,
    )


@pytest.fixture
def builder(db):
    # In your project a "builder" is a user with role "owner"
    return make_user("owner1", role="owner")


@pytest.fixture
def other_builder(db):
    return make_user("owner2", role="owner")


@pytest.fixture
def tenant(db):
    return make_user("tenant1", role="tenant")


@pytest.fixture
def admin(db):
    return make_user("admin1", role="owner", is_superuser=True, is_staff=True)


def _client_for(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def builder_client(builder):
    return _client_for(builder)


@pytest.fixture
def tenant_client(tenant):
    return _client_for(tenant)


@pytest.fixture
def admin_client(admin):
    return _client_for(admin)


@pytest.fixture
def anon_client():
    return APIClient()


@pytest.fixture
def make_property(db):
    """Creates a Property in the temporary test database."""
    def _make(owner, **overrides):
        data = {
            "property_name": "Sunrise Flat",
            "property_type": "flat",
            "address": "12 MG Road",
            "city": "Pune",
            "state": "Maharashtra",
            "rent": 20000,
            "deposit": 40000,
            "bedrooms": 2,
            "bathrooms": 2,
        }
        data.update(overrides)
        return Property.objects.create(owner=owner, **data)
    return _make