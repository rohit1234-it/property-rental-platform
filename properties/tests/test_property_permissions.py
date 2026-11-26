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


# ---------- Authentication ----------

def test_unauthenticated_user_is_rejected(anon_client):
    response = anon_client.get(URL)
    assert response.status_code in (401, 403)


# ---------- Create ----------

def test_builder_can_create_property(builder_client, builder):
    response = builder_client.post(URL, VALID_PAYLOAD, format="json")

    assert response.status_code == 201
    assert Property.objects.count() == 1
    assert Property.objects.get().owner == builder


def test_create_fails_when_required_fields_missing(builder_client):
    response = builder_client.post(URL, {"property_name": "Only name"}, format="json")

    assert response.status_code == 400
    assert Property.objects.count() == 0


# ---------- List ----------

def test_builder_sees_only_own_properties(
    builder_client, builder, other_builder, make_property
):
    make_property(builder, property_name="My Flat")
    make_property(other_builder, property_name="Stranger Flat")

    response = builder_client.get(URL)

    assert response.status_code == 200
    assert "My Flat" in str(response.data)
    assert "Stranger Flat" not in str(response.data)


def test_admin_sees_all_properties(
    admin_client, builder, other_builder, make_property
):
    make_property(builder, property_name="My Flat")
    make_property(other_builder, property_name="Stranger Flat")

    response = admin_client.get(URL)

    assert response.status_code == 200
    assert "My Flat" in str(response.data)
    assert "Stranger Flat" in str(response.data)


# ---------- Retrieve ----------

def test_owner_can_retrieve_own_property(builder_client, builder, make_property):
    prop = make_property(builder)

    response = builder_client.get(detail_url(prop.pk))

    assert response.status_code == 200


def test_cannot_retrieve_someone_elses_property(
    builder_client, other_builder, make_property
):
    prop = make_property(other_builder)

    response = builder_client.get(detail_url(prop.pk))

    assert response.status_code == 403


def test_retrieve_missing_property_returns_404(builder_client):
    response = builder_client.get(detail_url(99999))

    assert response.status_code == 404


# ---------- Update ----------

def test_owner_can_partially_update_property(builder_client, builder, make_property):
    prop = make_property(builder, rent=20000)

    response = builder_client.patch(
        detail_url(prop.pk), {"rent": 25000}, format="json"
    )

    assert response.status_code == 200
    prop.refresh_from_db()
    assert prop.rent == 25000