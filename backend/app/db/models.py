from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .session import Base

MealIngredient = Table(
    "meal_ingredient",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("meal_id", Integer, ForeignKey("meal.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id")),
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


class UserDietRequirements(Base):
    __tablename__ = "user_diet_requirements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)
    is_dairy_free = Column(Boolean, default=False)
    is_nut_free = Column(Boolean, default=False)
    is_shellfish_free = Column(Boolean, default=False)
    is_pescatarian = Column(Boolean, default=False)


class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    alias = Column(String)


class Meal(Base):
    __tablename__ = "meal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))

    ingredients = relationship(
        "Ingredient",
        secondary=MealIngredient,
        back_populates="meals",
    )
