import time
import falcon
import pytest
from falcon import testing
from firefalcon.firestore import FirstoreBaseResource


create = {"name": "John Smith", "dob": "01/03/2000"}
update = {"name": "John Walker"}
replace = {"name": "Marry Jones", "dob": "01/03/1920"}


@pytest.fixture(scope="module")
def client(db):
    user = FirstoreBaseResource(db=db, resource_type="user")
    api = falcon.API()

    api.add_route("/users", user)
    api.add_route("/users/{user_id}", user, suffix="doc")

    return testing.TestClient(api)


@pytest.yield_fixture(scope="module")
def user_id(client):
    response = client.simulate_post("/users", json=create)
    user = response.json
    print(response.text)
    yield user.get("data").get("id")


def test_get_user_collection(client, user_id):
    time.sleep(3)
    response = client.simulate_get(f"/users")
    print(response.json)
    assert response.status == falcon.HTTP_200


def test_patch_user_doc(client, user_id):
    response = client.simulate_patch(f"/users/{user_id}", json=update)
    print(response.text)
    assert response.status == falcon.HTTP_200


def test_put_user_doc(client, user_id):
    response = client.simulate_put(f"/users/{user_id}", json=replace)
    print(response.text)
    assert response.status == falcon.HTTP_200


def test_delete_user_doc(client, user_id):
    response = client.simulate_delete(f"/users/{user_id}")
    print(response.text)
    assert response.status == falcon.HTTP_200
