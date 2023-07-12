import typing as t

from app.core import security
from app.core.auth import get_current_active_superuser, get_current_active_user
from app.db.crud import (create_ingredient, delete_ingredient, edit_ingredient,
                         get_ingredient, get_ingredients)
from app.db.schemas import Ingredient, IngredientCreate, IngredientEdit
from app.db.session import get_db
from fastapi import APIRouter, Depends, Request, Response

ingredients_router = r = APIRouter()


@r.get(
    "/ingredients",
    response_model=t.List[Ingredient],
    response_model_exclude_none=True,
)
async def ingredients_list(
    response: Response,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get all ingredients
    """
    ingredients = get_ingredients(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(ingredients)}"
    return ingredients


@r.get(
    "/ingredients/{ingredient_id}",
    response_model=Ingredient,
    response_model_exclude_none=True,
)
async def ingredient_by_id(
    request: Request,
    ingredient_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get any ingredient by id
    """
    return get_ingredient(db, ingredient_id)


@r.post(
    "/ingredients",
    response_model=Ingredient,
    response_model_exclude_none=True,
)
async def ingredient_create(
    request: Request,
    ingredient: IngredientCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Create a new ingredient
    """
    return create_ingredient(db, ingredient)


@r.put(
    "/ingredients/{ingredient_id}",
    response_model=Ingredient,
    response_model_exclude_none=True,
)
async def ingredient_edit(
    request: Request,
    ingredient_id: int,
    ingredient: IngredientEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Edit an ingredient
    """
    return edit_ingredient(db, ingredient_id, ingredient)


@r.delete(
    "/ingredients/{ingredient_id}",
    response_model=Ingredient,
    response_model_exclude_none=True,
)
async def ingredient_delete(
    request: Request,
    ingredient_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Delete an ingredient
    """
    return delete_ingredient(db, ingredient_id)
