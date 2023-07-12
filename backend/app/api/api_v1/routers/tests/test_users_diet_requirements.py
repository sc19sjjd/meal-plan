from app.db import models


def test_get_user_diet_requirements(
    client, test_db, test_user, superuser_token_headers
):
    response = client.get(
        f"/api/v1/users_diet_requirements/{test_user.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200  #
    db_diet_requirements = (
        test_db.query(models.UserDietRequirements)
        .filter(models.UserDietRequirements.user_id == test_user.id)
        .first()
    )
    assert response.json() == {
        "id": db_diet_requirements.id,
        "user_id": db_diet_requirements.user_id,
        "is_vegetarian": db_diet_requirements.is_vegetarian,
        "is_vegan": db_diet_requirements.is_vegan,
        "is_gluten_free": db_diet_requirements.is_gluten_free,
        "is_dairy_free": db_diet_requirements.is_dairy_free,
        "is_nut_free": db_diet_requirements.is_nut_free,
        "is_shellfish_free": db_diet_requirements.is_shellfish_free,
        "is_pescatarian": db_diet_requirements.is_pescatarian,
    }


def test_get_user_diet_requirements_not_found(client, superuser_token_headers):
    response = client.get(
        f"/api/v1/users_diet_requirements/4321",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_get_user_diet_requirements_me(
    client, test_db, test_user, user_token_headers
):
    response = client.get(
        "/api/v1/users_diet_requirements/me",
        headers=user_token_headers,
    )
    assert response.status_code == 200  #
    db_diet_requirements = (
        test_db.query(models.UserDietRequirements)
        .filter(models.UserDietRequirements.user_id == test_user.id)
        .first()
    )
    assert response.json() == {
        "id": db_diet_requirements.id,
        "user_id": db_diet_requirements.user_id,
        "is_vegetarian": db_diet_requirements.is_vegetarian,
        "is_vegan": db_diet_requirements.is_vegan,
        "is_gluten_free": db_diet_requirements.is_gluten_free,
        "is_dairy_free": db_diet_requirements.is_dairy_free,
        "is_nut_free": db_diet_requirements.is_nut_free,
        "is_shellfish_free": db_diet_requirements.is_shellfish_free,
        "is_pescatarian": db_diet_requirements.is_pescatarian,
    }


def test_edit_user_diet_requirements(
    client, test_db, test_user, superuser_token_headers
):
    new_diet_requirements = {
        "is_vegetarian": True,
        "is_vegan": True,
        "is_gluten_free": True,
        "is_dairy_free": True,
        "is_nut_free": True,
        "is_shellfish_free": True,
        "is_pescatarian": True,
    }

    response = client.put(
        f"/api/v1/users_diet_requirements/{test_user.id}",
        json=new_diet_requirements,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    db_diet_requirements = (
        test_db.query(models.UserDietRequirements)
        .filter(models.UserDietRequirements.user_id == test_user.id)
        .first()
    )
    new_diet_requirements["id"] = db_diet_requirements.id
    new_diet_requirements["user_id"] = db_diet_requirements.user_id
    assert response.json() == new_diet_requirements


def test_edit_user_diet_requirements_not_found(client, superuser_token_headers):
    new_diet_requirements = {
        "is_vegetarian": True,
        "is_vegan": True,
        "is_gluten_free": True,
        "is_dairy_free": True,
        "is_nut_free": True,
        "is_shellfish_free": True,
        "is_pescatarian": True,
    }

    response = client.put(
        f"/api/v1/users_diet_requirements/4321",
        json=new_diet_requirements,
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_edit_user_diet_requirements_me(
    client, test_db, test_user, user_token_headers
):
    new_diet_requirements = {
        "is_vegetarian": True,
        "is_vegan": True,
        "is_gluten_free": True,
        "is_dairy_free": True,
        "is_nut_free": True,
        "is_shellfish_free": True,
        "is_pescatarian": True,
    }

    response = client.put(
        "/api/v1/users_diet_requirements/me",
        json=new_diet_requirements,
        headers=user_token_headers,
    )
    assert response.status_code == 200
    db_diet_requirements = (
        test_db.query(models.UserDietRequirements)
        .filter(models.UserDietRequirements.user_id == test_user.id)
        .first()
    )
    new_diet_requirements["id"] = db_diet_requirements.id
    new_diet_requirements["user_id"] = db_diet_requirements.user_id
    assert response.json() == new_diet_requirements


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/users_diet_requirements/me")
    assert response.status_code == 401
    response = client.get("/api/v1/users_diet_requirements/1")
    assert response.status_code == 401
    response = client.put("/api/v1/users_diet_requirements/me")
    assert response.status_code == 401
    response = client.put("/api/v1/users_diet_requirements/1")
    assert response.status_code == 401


def test_unauthorized_routes(client, user_token_headers):
    response = client.get(
        "/api/v1/users_diet_requirements/1", headers=user_token_headers
    )
    assert response.status_code == 403
    response = client.put(
        "/api/v1/users_diet_requirements/1", headers=user_token_headers
    )
    assert response.status_code == 403
