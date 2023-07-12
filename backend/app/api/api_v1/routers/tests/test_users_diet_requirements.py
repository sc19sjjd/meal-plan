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
