from app.db import models


def test_get_users(client, test_superuser, superuser_token_headers):
    response = client.get("/api/v1/users", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_superuser.id,
            "email": test_superuser.email,
            "is_active": test_superuser.is_active,
            "is_superuser": test_superuser.is_superuser,
            "is_verified": test_superuser.is_verified,
        }
    ]


def test_delete_user(client, test_superuser, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/users/{test_superuser.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.User).all() == []


def test_delete_user_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/users/4321", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_edit_user(client, test_user, superuser_token_headers):
    new_user = {
        "email": "newemail@test.com",
        "is_active": False,
        "is_superuser": True,
        "is_verified": True,
        "name": "Joe Smith",
        "password": "new_password",
    }

    response = client.put(
        f"/api/v1/users/{test_user.id}",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_user["id"] = test_user.id
    new_user.pop("password")
    assert response.json() == new_user


def test_edit_user_not_found(client, superuser_token_headers):
    new_user = {
        "email": "newemail@test.com",
        "is_active": False,
        "is_superuser": False,
        "is_verified": False,
        "password": "new_password",
    }
    response = client.put(
        "/api/v1/users/1234", json=new_user, headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_edit_user_invalid_email(client, test_user, superuser_token_headers):
    new_user = {
        "email": "newemail.com",
    }
    response = client.put(
        f"/api/v1/users/{test_user.id}",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 400
    new_user = {
        "email": "@test.com",
    }
    response = client.put(
        f"/api/v1/users/{test_user.id}",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 400


def test_edit_user_me(client, test_user, user_token_headers):
    new_user = {
        "email": "newemail@test.com",
        "is_active": False,
        "is_superuser": False,
        "is_verified": False,
        "password": "new_password",
    }
    response = client.put(
        "/api/v1/users/me", json=new_user, headers=user_token_headers
    )
    assert response.status_code == 200
    new_user["id"] = test_user.id
    new_user.pop("password")
    assert response.json() == new_user


def test_get_user(
    client,
    test_user,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/users/{test_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_user.id,
        "email": test_user.email,
        "is_active": bool(test_user.is_active),
        "is_superuser": test_user.is_superuser,
        "is_verified": test_user.is_verified,
    }


def test_get_user_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/users/123", headers=superuser_token_headers)
    assert response.status_code == 404


def test_authenticated_user_me(client, user_token_headers):
    response = client.get("/api/v1/users/me", headers=user_token_headers)
    assert response.status_code == 200


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    response = client.get("/api/v1/users")
    assert response.status_code == 401
    response = client.get("/api/v1/users/123")
    assert response.status_code == 401
    response = client.put("/api/v1/users/me")
    assert response.status_code == 401
    response = client.put("/api/v1/users/123")
    assert response.status_code == 401
    response = client.delete("/api/v1/users/123")
    assert response.status_code == 401


def test_unauthorized_routes(client, user_token_headers):
    response = client.get("/api/v1/users", headers=user_token_headers)
    assert response.status_code == 403
    response = client.get("/api/v1/users/123", headers=user_token_headers)
    assert response.status_code == 403
    response = client.put("/api/v1/users/123", headers=user_token_headers)
    assert response.status_code == 403
    response = client.delete("/api/v1/users/123", headers=user_token_headers)
    assert response.status_code == 403
