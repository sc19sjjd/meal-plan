import typing as t

import email_validator
import pytest
from app.core import config, security
from app.db import models
from app.db.session import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

email_validator.TEST_ENVIRONMENT = True


def get_test_db_url() -> str:
    return f"{config.SQLALCHEMY_DATABASE_URI}_test"


@pytest.fixture
def test_db():
    """
    Modify the db session to automatically roll back after each test.
    This is to avoid tests affecting the database state of other tests.
    """
    # Connect to the test database
    test_engine = create_engine(
        get_test_db_url(),
        echo=False,
        # connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(bind=test_engine)
    session_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    SessionLocal = session_factory
    session = SessionLocal()

    yield session  # this is where the test function will execute

    # Teardown: rollback any changes made during the test and close the session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=test_engine)


# @pytest.fixture()
# def test_db():
#     """
#     Modify the db session to automatically roll back after each test.
#     This is to avoid tests affecting the database state of other tests.
#     """
#     # Connect to the test database
#     engine = create_engine(
#         get_test_db_url(),
#         echo=True,
#     )

#     connection = engine.connect()
#     trans = connection.begin()

#     # Run a parent transaction that can roll back all changes
#     test_session_maker = sessionmaker(
#         autocommit=False, autoflush=False, bind=engine
#     )
#     test_session = test_session_maker()
#     savepoint = test_session.begin_nested()
#     test_session.expire_all()
#     # print("begin nested")

#     @event.listens_for(test_session, "after_transaction_end")
#     def restart_savepoint(s, transaction):
#         if transaction.nested and not transaction._parent.nested:
#             s.expire_all()
#             s.begin_nested()
#             # print("new transaction")

#     # print(test_session._nested_transaction)
#     # print("before yield")

#     yield test_session

#     print("rollback")
#     # print(test_session._nested_transaction)
#     # print("before rollback")
#     # Roll back the parent transaction after the test is complete
#     #savepoint.rollback()
#     test_session.rollback()
#     test_session.close()
#     trans.rollback()
#     trans.close()
#     connection.close()
#     # print(test_session._nested_transaction)
#     # print("after rollback")


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """
    Create a test database and use it for the whole test session.
    """

    test_db_url = get_test_db_url()

    # Create the test database
    assert not database_exists(
        test_db_url
    ), "Test database already exists. Aborting tests."
    create_database(test_db_url)
    test_engine = create_engine(test_db_url)
    Base.metadata.create_all(test_engine)

    # Run the tests
    yield

    # Drop the test database
    drop_database(test_db_url)


@pytest.fixture
def client(test_db):
    """
    Get a TestClient instance that reads/write to the test database.
    """

    def get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app)


@pytest.fixture
def test_password() -> str:
    return "securepassword"


def get_password_hash() -> str:
    """
    Password hashing can be expensive so a mock will be much faster
    """
    return "supersecrethash"


@pytest.fixture
def test_user(test_db) -> models.User:
    """
    Make a test user in the database
    """
    user = models.User(
        email="fake@email.com",
        hashed_password=get_password_hash(),
        is_active=True,
        is_verified=True,
    )
    test_db.add(user)
    user_diet_requirements = models.UserDietRequirements(
        user_id=user.id,
    )
    test_db.add(user_diet_requirements)
    user.diet_requirements = user_diet_requirements
    test_db.commit()

    return user


@pytest.fixture
def test_superuser(test_db) -> models.User:
    """
    Superuser for testing
    """
    user = models.User(
        email="fakeadmin@email.com",
        hashed_password=get_password_hash(),
        is_superuser=True,
        is_verified=True,
    )
    test_db.add(user)
    user_diet_requirements = models.UserDietRequirements(
        user_id=user.id,
    )
    test_db.add(user_diet_requirements)
    user.diet_requirements = user_diet_requirements
    test_db.commit()

    return user


def verify_password_mock(first: str, second: str) -> bool:
    return True


@pytest.fixture
def user_token_headers(
    client: TestClient, test_user, test_password, monkeypatch
) -> t.Dict[str, str]:
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_user.email,
        "password": test_password,
    }
    r = client.post("/api/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture
def superuser_token_headers(
    client: TestClient, test_superuser, test_password, monkeypatch
) -> t.Dict[str, str]:
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_superuser.email,
        "password": test_password,
    }
    r = client.post("/api/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture
def test_ingredients(test_db) -> t.List[models.Ingredient]:
    """
    Make 2 test ingredients in the database
    """
    ingredients = []
    ingredients.append(models.Ingredient(name="Test Ingredient"))
    ingredients.append(models.Ingredient(name="Test Ingredient 2"))
    test_db.add(ingredients[0])
    test_db.add(ingredients[1])
    test_db.commit()
    return ingredients


@pytest.fixture
def test_meals(
    test_db, test_ingredients, test_user, test_superuser
) -> t.List[models.Meal]:
    """
    Make 3 test meals in the database
    """
    meals = []
    meals.append(
        models.Meal(
            name="Test Meal",
            description="Test Description",
            user_id=test_user.id,
        )
    )
    meals[0].ingredients.append(test_ingredients[0])
    meals[0].ingredients.append(test_ingredients[1])
    meals.append(
        models.Meal(
            name="Test Meal 2",
            description="Test Description 2",
            user_id=test_user.id,
        )
    )
    meals[1].ingredients.append(test_ingredients[0])
    meals.append(
        models.Meal(
            name="Test Meal 3",
            description="Test Description 3",
            user_id=test_superuser.id,
        )
    )
    test_db.add(meals[0])
    test_db.add(meals[1])
    test_db.add(meals[2])
    test_user.meals.append(meals[0])
    test_user.meals.append(meals[1])
    test_superuser.meals.append(meals[2])
    test_db.commit()
    return meals
