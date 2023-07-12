import typing as t

from app.core.security import get_password_hash
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int) -> schemas.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_verified=user.is_verified,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # corresponding user's diet requirements (default to all false)
    diet_requirements = schemas.UserDietRequirementsCreate()
    create_user_diet_requirements(db, db_user.id, diet_requirements)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_diet_requirements(
    db: Session, user_id: int
) -> schemas.UserDietRequirements:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user.diet_requirements


def create_user_diet_requirements(
    db: Session,
    user_id: int,
    diet_requirements: schemas.UserDietRequirementsCreate,
) -> schemas.UserDietRequirements:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    db_diet_requirements = models.UserDietRequirements(
        user_id=user_id,
        is_vegetarian=diet_requirements.is_vegetarian,
        is_vegan=diet_requirements.is_vegan,
        is_gluten_free=diet_requirements.is_gluten_free,
        is_dairy_free=diet_requirements.is_dairy_free,
        is_nut_free=diet_requirements.is_nut_free,
        is_shellfish_free=diet_requirements.is_shellfish_free,
        is_pescatarian=diet_requirements.is_pescatarian,
    )
    db.add(db_diet_requirements)
    db.commit()
    db.refresh(db_diet_requirements)
    return db_diet_requirements


def edit_user_diet_requirements(
    db: Session,
    user_id: int,
    diet_requirements: schemas.UserDietRequirementsEdit,
) -> schemas.UserDietRequirements:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    db_diet_requirements = db_user.diet_requirements
    if not db_diet_requirements:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Diet requirements not found"
        )

    update_data = diet_requirements.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_diet_requirements, key, value)

    db.add(db_diet_requirements)
    db.commit()
    db.refresh(db_diet_requirements)
    return db_diet_requirements


def get_ingredient(db: Session, ingredient_id: int) -> schemas.Ingredient:
    ingredient = (
        db.query(models.Ingredient)
        .filter(models.Ingredient.id == ingredient_id)
        .first()
    )
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


def get_ingredient_by_name(db: Session, name: str) -> schemas.Ingredient:
    return (
        db.query(models.Ingredient)
        .filter(models.Ingredient.name == name)
        .first()
    )


def get_ingredients(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.Ingredient]:
    return db.query(models.Ingredient).offset(skip).limit(limit).all()


def create_ingredient(
    db: Session, ingredient: schemas.IngredientCreate
) -> schemas.Ingredient:
    db_ingredient = models.Ingredient(
        name=ingredient.name,
        alias=ingredient.alias,
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


def delete_ingredient(db: Session, ingredient_id: int) -> schemas.Ingredient:
    ingredient = get_ingredient(db, ingredient_id)
    if not ingredient:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Ingredient not found"
        )
    db.delete(ingredient)
    db.commit()
    return ingredient


def edit_ingredient(
    db: Session, ingredient_id: int, ingredient: schemas.IngredientEdit
) -> schemas.Ingredient:
    db_ingredient = get_ingredient(db, ingredient_id)
    if not db_ingredient:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Ingredient not found"
        )
    update_data = ingredient.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_ingredient, key, value)

    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


def get_meal(db: Session, meal_id: int) -> schemas.Meal:
    meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


def get_meals(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.Meal]:
    return db.query(models.Meal).offset(skip).limit(limit).all()


def create_meal(db: Session, meal: schemas.MealCreate) -> schemas.Meal:
    db_meal = models.Meal(
        name=meal.name,
        description=meal.description,
    )
    db.add(db_meal)
    db.commit()

    for ingredient_id in meal.ingredients:
        db_ingredient = db.query(models.Ingredient).get(ingredient_id)
        if db_ingredient is not None:
            db_meal.ingredients.append(db_ingredient)

    db.commit()
    db.refresh(db_meal)
    return db_meal


def delete_meal(db: Session, meal_id: int) -> schemas.Meal:
    meal = get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Meal not found")
    db.delete(meal)
    db.commit()
    return meal


def edit_meal(
    db: Session, meal_id: int, meal: schemas.MealEdit
) -> schemas.Meal:
    db_meal = get_meal(db, meal_id)
    if not db_meal:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Meal not found")
    update_data = meal.dict(exclude_unset=True)

    if "ingredients" in update_data:
        db_meal.ingredients = []

        # pop ingredients to remove them from update_data
        for ingredient_id in update_data.pop("ingredients"):
            db_ingredient = db.query(models.Ingredient).get(ingredient_id)
            if db_ingredient is not None:
                db_meal.ingredients.append(db_ingredient)

    for key, value in update_data.items():
        setattr(db_meal, key, value)

    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal
