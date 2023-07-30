from app.db import models


def test_get_ingredients_list(client, test_ingredients, user_token_headers):
    response = client.get(
        f"/api/v1/ingredients",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_ingredients[0].id,
            "name": test_ingredients[0].name,
        },
        {
            "id": test_ingredients[1].id,
            "name": test_ingredients[1].name,
        }
    ]


def test_get_ingredients_by_name(client, test_ingredients, user_token_headers):
    response = client.get(
        f"/api/v1/ingredients?name=Test%20Ingredient%20",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    response = client.get(
        f"/api/v1/ingredients?name={test_ingredients[0].name}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_ingredients[0].id,
            "name": test_ingredients[0].name,
        }
    ]


def test_get_ingredient(client, test_ingredients, superuser_token_headers):
    response = client.get(
        f"/api/v1/ingredients/{test_ingredients[0].id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_ingredients[0].id,
        "name": test_ingredients[0].name,
    }


def test_get_ingredient_not_found(client, test_ingredients, superuser_token_headers):
    response = client.get(
        f"/api/v1/ingredients/4321",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_create_ingredient(client, superuser_token_headers):
    new_ingredient = {
        "name": "Test Ingredient",
    }

    response = client.post(
        "/api/v1/ingredients/", json=new_ingredient, headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Ingredient",
    }


def test_create_ingredient_duplicate(client, test_ingredients, superuser_token_headers):
    new_ingredient = {
        "name": "Test Ingredient",
    }

    response = client.post(
        "/api/v1/ingredients/", json=new_ingredient, headers=superuser_token_headers
    )
    assert response.status_code == 400


def test_edit_ingredient(client, test_ingredients, superuser_token_headers):
    new_ingredient = {
        "name": "New Test Ingredient",
        "alias": "Test Ingredient Alias",
    }

    response = client.put(
        f"/api/v1/ingredients/{test_ingredients[0].id}",
        json=new_ingredient,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_ingredient["id"] = test_ingredients[0].id
    assert response.json() == new_ingredient


def test_edit_ingredient_not_found(client, test_ingredients, superuser_token_headers):
    new_ingredient = {
        "name": "New Test Ingredient",
        "alias": "Test Ingredient Alias",
    }

    response = client.put(
        f"/api/v1/ingredients/4321",
        json=new_ingredient,
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_edit_ingredient_duplicate(client, test_ingredients, superuser_token_headers):
    new_ingredient = {
        "name": "Test Ingredient 2",
        "alias": "Test Ingredient 2 Alias",
    }

    response = client.put(
        f"/api/v1/ingredients/{test_ingredients[0].id}",
        json=new_ingredient,
        headers=superuser_token_headers,
    )
    assert response.status_code == 400


def test_delete_ingredient(client, test_db, test_ingredients, superuser_token_headers):
    response = client.delete(
        f"/api/v1/ingredients/{test_ingredients[0].id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_ingredients[0].id,
        "name": test_ingredients[0].name,
    }
    assert test_db.query(models.Ingredient).get(test_ingredients[0].id) is None


def test_delete_ingredient_not_found(client, test_ingredients, superuser_token_headers):
    response = client.delete(
        f"/api/v1/ingredients/4321",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/ingredients")
    assert response.status_code == 401
    response = client.get("/api/v1/ingredients/1")
    assert response.status_code == 401
    response = client.post("/api/v1/ingredients")
    assert response.status_code == 401
    response = client.put("/api/v1/ingredients/1")
    assert response.status_code == 401
    response = client.delete("/api/v1/ingredients/1")
    assert response.status_code == 401


def test_unauthorized_routes(client, user_token_headers):
    response = client.get("/api/v1/ingredients/1", headers=user_token_headers)
    assert response.status_code == 403
    response = client.post(
        "/api/v1/ingredients",
        headers=user_token_headers,
    )
    assert response.status_code == 403
    response = client.put(
        "/api/v1/ingredients/1",
        headers=user_token_headers,
    )
    assert response.status_code == 403
    response = client.delete