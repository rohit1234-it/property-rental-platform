from properties.models.property import Property

URL = "/api/property/"

VALID_PAYLOAD = {
    "property_name": "Green Villa",
    "property_type": "house",
    "address": "5 FC Road",
    "city": "Pune",
    "state": "Maharashtra",
    "rent": 35000,
    "deposit": 70000,
    "bedrooms": 3,
    "bathrooms": 2,
}


def detail_url(pk):
    return f"{URL}{pk}/"


def test_cannot_update_someone_elses_property(
    builder_client, other_builder, make_property
):
    prop = make_property(other_builder, rent=20000)

    response = builder_client.patch(
        detail_url(prop.pk), {"rent": 1}, format="json"
    )

    assert response.status_code == 403
    prop.refresh_from_db()
    assert prop.rent == 20000


def test_builder_cannot_delete_property(builder_client, builder, make_property):
    prop = make_property(builder)

    response = builder_client.delete(detail_url(prop.pk))

    assert response.status_code == 403
    assert Property.objects.count() == 1


def test_admin_can_delete_property(admin_client, builder, make_property):
    prop = make_property(builder)

    response = admin_client.delete(detail_url(prop.pk))

    assert response.status_code == 200
    assert Property.objects.count() == 0


def test_tenant_cannot_create_property(tenant_client):
    response = tenant_client.post(URL, VALID_PAYLOAD, format="json")

    assert response.status_code == 403