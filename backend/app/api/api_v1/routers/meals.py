import typing as t

from app.core import security
from app.core.auth import get_current_active_superuser, get_current_active_user
from app.db.crud import (create_meal, delete_meal, edit_meal, get_all_meals,
                         get_meal, get_meals_like_name, object_as_dict)
from app.db.schemas import Meal, MealCreate, MealEdit, MealOut
from app.db.session import get_db
from fastapi import APIRouter, Depends, Query, Request, Response

meals_router = r = APIRouter()


@r.get(
    "/meals/me",
    response_model=t.List[Meal],
    response_model_exclude_none=True,
)
async def meals_list(
    response: Response,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
    name: t.Annotated[str | None, Query(max_length=50)] = None,
):
    """
    Get all current user's meals
    """
    if name:
        meals = get_meals_like_name(db, name, user_id=current_user.id)
    else:
        meals = get_all_meals(db, user_id=current_user.id)

    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(meals)}"
    return meals


@r.get(
    "/meals/{meal_id}",
    response_model=Meal,
    response_model_exclude_none=True,
)
async def meal_by_id(
    request: Request,
    meal_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get any meal by id
    """
    return get_meal(db, meal_id)


@r.post(
    "/meals",
    response_model=Meal,
    response_model_exclude_none=True,
)
async def meal_create(
    request: Request,
    meal_create: MealCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create new meal
    """
    return create_meal(db, meal_create, current_user.id)


@r.put(
    "/meals/{meal_id}",
    response_model=Meal,
    response_model_exclude_none=True,
)
async def meal_edit(
    request: Request,
    meal_id: int,
    meal_edit: MealEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Edit meal
    """
    return edit_meal(db, meal_id, meal_edit, current_user.id)


@r.delete(
    "/meals/{meal_id}",
    response_model=Meal,
    response_model_exclude_none=True,
)
async def meal_delete(
    request: Request,
    meal_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Delete existing meal
    """
    return delete_meal(db, meal_id, current_user.id)
