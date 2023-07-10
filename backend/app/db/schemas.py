import typing as t

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    name: str = None


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    email: t.Optional[str] = None
    name: t.Optional[str] = None
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"


class UserDietRequirementsBase(BaseModel):
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_dairy_free: bool = False
    is_nut_free: bool = False
    is_shellfish_free: bool = False
    is_pescatarian: bool = False


class UserDietRequirementsOut(UserDietRequirementsBase):
    pass


class UserDietRequirementsCreate(UserDietRequirementsBase):
    class Config:
        orm_mode = True


class UserDietRequirementsEdit(UserDietRequirementsBase):
    is_vegetarian: t.Optional[bool] = None
    is_vegan: t.Optional[bool] = None
    is_gluten_free: t.Optional[bool] = None
    is_dairy_free: t.Optional[bool] = None
    is_nut_free: t.Optional[bool] = None
    is_shellfish_free: t.Optional[bool] = None
    is_pescatarian: t.Optional[bool] = None

    class Config:
        orm_mode = True


class UserDietRequirements(UserDietRequirementsBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class IngredientBase(BaseModel):
    name: str
    alias: str = None


class IngredientOut(IngredientBase):
    pass


class IngredientCreate(IngredientBase):
    class Config:
        orm_mode = True


class IngredientEdit(IngredientBase):
    name: t.Optional[str] = None
    alias: t.Optional[str] = None

    class Config:
        orm_mode = True


class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True


class MealBase(BaseModel):
    name: str
    description: str = None


class MealOut(MealBase):
    ingredients: t.List[IngredientOut] = []

    class Config:
        orm_mode = True


class MealCreate(MealBase):
    ingredients: t.List[int] = []

    class Config:
        orm_mode = True


class MealEdit(MealBase):
    name: t.Optional[str] = None
    description: t.Optional[str] = None
    ingredients: t.Optional[t.List[int]] = None

    class Config:
        orm_mode = True


class Meal(MealBase):
    id: int
    user_id: int
    ingredients: t.List[Ingredient] = []

    class Config:
        orm_mode = True
