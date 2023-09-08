from app.db import models


def test_get_meals_me(client, test_user, test_meals, user_token_headers):
    response = client.get(
        "/api/v1/meals/me",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_meals[0].id,
            "name": test_meals[0].name,
            "user_id": test_user.id,
            "description": test_meals[0].description,
            "ingredients": [
                {
                    "id": test_meals[0].ingredients[0].id,
                    "name": test_meals[0].ingredients[0].name,
                },
                {
                    "id": test_meals[0].ingredients[1].id,
                    "name": test_meals[0].ingredients[1].name,
                },
            ],
        },
        {
            "id": test_meals[1].id,
            "name": test_meals[1].name,
            "user_id": test_user.id,
            "description": test_meals[1].description,
            "ingredients": [
                {
                    "id": test_meals[1].ingredients[0].id,
                    "name": test_meals[1].ingredients[0].name,
                },
            ],
        },
    ]


def test_get_meals_by_name(client, test_user, test_meals, user_token_headers):
    response = client.get(
        f"/api/v1/meals/me?name=Test%20Meal",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    response = client.get(
        f"/api/v1/meals/me?name={test_meals[1].name}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_meals[1].id,
            "name": test_meals[1].name,
            "user_id": test_user.id,
            "description": test_meals[1].description,
            "ingredients": [
                {
                    "id": test_meals[1].ingredients[0].id,
                    "name": test_meals[1].ingredients[0].name,
                },
            ],
        },
    ]


def test_get_meal(client, test_user, test_meals, superuser_token_headers):
    response = client.get(
        f"/api/v1/meals/{test_meals[0].id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_meals[0].id,
        "name": test_meals[0].name,
        "user_id": test_user.id,
        "description": test_meals[0].description,
        "ingredients": [
            {
                "id": test_meals[0].ingredients[0].id,
                "name": test_meals[0].ingredients[0].name,
            },
            {
                "id": test_meals[0].ingredients[1].id,
                "name": test_meals[0].ingredients[1].name,
            },
        ],
    }


def test_get_meal_not_found(client, test_meals, superuser_token_headers):
    response = client.get(
        f"/api/v1/meals/4321",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_create_meal(client, test_user, test_ingredients, user_token_headers):
    new_meal = {
        "name": "New Meal",
        "description": "New Description",
        "ingredients": [
            test_ingredients[0].id,
        ],
    }

    response = client.post(
        "/api/v1/meals",
        json=new_meal,
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": new_meal["name"],
        "user_id": test_user.id,
        "description": new_meal["description"],
        "ingredients": [
            {
                "id": test_ingredients[0].id,
                "name": test_ingredients[0].name,
            },
        ],
    }


def test_create_meal_duplicate(
    client, test_meals, test_ingredients, user_token_headers
):
    new_meal = {
        "name": test_meals[0].name,
        "description": "New Description",
        "ingredients": [
            test_ingredients[0].id,
        ],
    }

    response = client.post(
        "/api/v1/meals",
        json=new_meal,
        headers=user_token_headers,
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Meal with this name already exists"}


def test_create_meal_invalid_ingredient(
    client, test_ingredients, user_token_headers
):
    new_meal = {
        "name": "New Meal",
        "description": "New Description",
        "ingredients": [
            1234,
        ],
    }

    response = client.post(
        "/api/v1/meals",
        json=new_meal,
        headers=user_token_headers,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Ingredient not found"}


def test_edit_meal(
    client, test_user, test_meals, test_ingredients, user_token_headers
):
    new_meal = {
        "name": "New Meal",
        "description": "New Description",
        "ingredients": [
            test_ingredients[0].id,
        ],
    }

    response = client.put(
        f"/api/v1/meals/{test_meals[0].id}",
        json=new_meal,
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_meals[0].id,
        "name": new_meal["name"],
        "user_id": test_user.id,
        "description": new_meal["description"],
        "ingredients": [
            {
                "id": test_ingredients[0].id,
                "name": test_ingredients[0].name,
            },
        ],
    }


def test_edit_meal_not_found(client, user_token_headers):
    new_meal = {
        "name": "New Meal",
        "description": "New Description",
    }

    response = client.put(
        f"/api/v1/meals/4321",
        json=new_meal,
        headers=user_token_headers,
    )
    assert response.status_code == 404


def test_edit_meal_duplicate(client, test_meals, user_token_headers):
    new_meal = {
        "name": test_meals[1].name,
        "description": "New Description",
    }

    response = client.put(
        f"/api/v1/meals/{test_meals[0].id}",
        json=new_meal,
        headers=user_token_headers,
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Meal with this name already exists"}


def test_edit_meal_invalid_ingredient(client, test_meals, user_token_headers):
    new_meal = {
        "name": "New Meal",
        "description": "New Description",
        "ingredients": [
            1234,
        ],
    }

    response = client.put(
        f"/api/v1/meals/{test_meals[0].id}",
        json=new_meal,
        headers=user_token_headers,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Ingredient not found"}


def test_edit_meal_unowned(client, test_meals, user_token_headers):
    new_meal = {
        "name": "New Meal",
        "description": "New Description",
    }

    response = client.put(
        f"/api/v1/meals/{test_meals[2].id}",
        json=new_meal,
        headers=user_token_headers,
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not authorized to edit this meal"
    }


def test_delete_meal(client, test_meals, user_token_headers):
    response = client.delete(
        f"/api/v1/meals/{test_meals[0].id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_meals[0].id,
        "name": test_meals[0].name,
        "user_id": test_meals[0].user_id,
        "description": test_meals[0].description,
        "ingredients": [
            {
                "id": test_meals[0].ingredients[0].id,
                "name": test_meals[0].ingredients[0].name,
            },
            {
                "id": test_meals[0].ingredients[1].id,
                "name": test_meals[0].ingredients[1].name,
            },
        ],
    }


def test_delete_meal_not_found(client, test_meals, user_token_headers):
    response = client.delete(
        f"/api/v1/meals/4321",
        headers=user_token_headers,
    )
    assert response.status_code == 404


def test_delete_meal_unowned(client, test_meals, user_token_headers):
    response = client.delete(
        f"/api/v1/meals/{test_meals[2].id}",
        headers=user_token_headers,
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not authorized to delete this meal"
    }


def test_unauthenticated_routes(client):
    response = client.get(f"/api/v1/meals/1")
    assert response.status_code == 401
    response = client.get("/api/v1/meals/me")
    assert response.status_code == 401
    response = client.post("/api/v1/meals")
    assert response.status_code == 401
    response = client.put(f"/api/v1/meals/1")
    assert response.status_code == 401
    response = client.delete(f"/api/v1/meals/1")
    assert response.status_code == 401


def test_unauthorized_routes(client, user_token_headers):
    response = client.get(f"/api/v1/meals/1", headers=user_token_headers)
    assert response.status_code == 403
