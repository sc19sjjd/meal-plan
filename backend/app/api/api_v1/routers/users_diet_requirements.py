from app.core import security
from app.core.auth import get_current_active_superuser, get_current_active_user
from app.db.crud import edit_user_diet_requirements, get_user_diet_requirements
from app.db.schemas import UserDietRequirements, UserDietRequirementsEdit
from app.db.session import get_db
from fastapi import APIRouter, Depends, Request

users_diet_router = r = APIRouter()


@r.get(
    "/users_diet_requirements/me",
    response_model=UserDietRequirements,
    response_model_exclude_none=True,
)
async def user_diet_requirements_me(
    current_user=Depends(get_current_active_user),
):
    """
    Get current user diet requirements
    """
    return current_user.diet_requirements


@r.get(
    "/users_diet_requirements/{user_id}",
    response_model=UserDietRequirements,
    response_model_exclude_none=True,
)
async def user_diet_requirements_by_id(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get any user diet requirements by user id
    """
    user_diet_requirements = get_user_diet_requirements(db, user_id)
    return user_diet_requirements


@r.put(
    "/users_diet_requirements/me",
    response_model=UserDietRequirements,
    response_model_exclude_none=True,
)
async def user_diet_requirements_edit_me(
    request: Request,
    user_diet_requirements_edit: UserDietRequirementsEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update current user diet requirements
    """
    user_diet_requirements = edit_user_diet_requirements(
        db, current_user.id, user_diet_requirements_edit
    )
    return user_diet_requirements


@r.put(
    "/users_diet_requirements/{user_id}",
    response_model=UserDietRequirements,
    response_model_exclude_none=True,
)
async def user_diet_requirements_edit_by_id(
    request: Request,
    user_id: int,
    user_diet_requirements_edit: UserDietRequirementsEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Update any user diet requirements by user id
    """
    user_diet_requirements = edit_user_diet_requirements(
        db, user_id, user_diet_requirements_edit
    )
    return user_diet_requirements
