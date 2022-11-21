from fastapi.testclient import TestClient
import random
import string
from main import app
from faker import Faker
from pytest import fixture


@fixture(scope="session", autouse=True)
def cli():
    with TestClient(app) as cli:
        yield cli



fake = Faker()


def random_lower(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def random_multi(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


def create_user():
    return {
      "email": random_lower(10)+"@rowmate.org",
      "avatar": {
        "is_circle": True,
        "topType": "NoHair",
        "accessoriesType": "Blank",
        "hairColor": "Black",
        "facialHairType": "Blank",
        "clotheType": "BlazerShirt",
        "eyeType": "Default",
        "eyebrowType": "Default",
        "mouthType": "Default",
        "skinColor": "Light",
        "topColor": "Black",
        "graphicType": "Deer",
        "facialHairColor": "Black",
        "clotheColor": "Black",
        "circleColor": "6fb8e0"
      },
      "password": random_multi(12),
      "yob": random.randint(1950,2003),
      "lang": "de-CH",
      "firstname": fake.first_name(),
      "lastname": fake.last_name(),
      "is_active": False,
      "is_superuser": False,
      "is_verified": False,
      "is_accepted": False,
      "roles": [
        "User"
      ]
    }


users = [create_user() for _ in range(10)]
users[1]["email"] = users[0]["email"]  # user 1 email is same as user 0 email


def test_register(cli):
    response = cli.post("/auth/register", json=users[0])
    assert response.json()["avatar"] == users[0]["avatar"]
    assert response.status_code == 201


def test_register_existing(cli):
    response = cli.post("/auth/register", json=users[1])
    assert response.status_code == 400


def test_register_active_superuser(cli):
    user = create_user()
    user["is_active"] = True
    user["is_superuser"] = True
    user["is_verified"] = True
    user["is_accepted"] = True

    response = cli.post("/auth/register", json=user)
    assert response.status_code == 422


def test_register_admin(cli):
    user = create_user()
    user["roles"] = ["User", "Manager", "Admin"]
    response = cli.post("/auth/register", json=user)
    assert response.status_code == 422


def test_get_config(cli):
    response = cli.get("/config")
    assert response.status_code == 200

