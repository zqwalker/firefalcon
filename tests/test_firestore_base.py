import falcon
import pytest
from falcon import testing
from firefalcon.firestore import FirstoreBaseResource


create = {"name": "John Smith", "dob": "01/03/2000"}

update = {"name": "John Walker"}

replace = {"name": "Marry Jones", "dob": "01/03/1920"}


@pytest.fixture
def client(db):
    user = FirstoreBaseResource(db=db)
    api = falcon.API()
    api.add_route("/users", user)
    return testing.TestClient(api)


@pytest.fixture
def user_id(client):
    return client.simulate_post("/users", json=create)


def test_get_user_collection(client, user_id):
    user = user_id.json()
    response = client.simulate_get(f"/users/{user.get('id')}")
    assert response.status == falcon.HTTP_200
