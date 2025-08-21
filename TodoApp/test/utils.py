from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from TodoApp.database import Base
from TodoApp.main import app
from fastapi.testclient import TestClient
import pytest
from TodoApp.models import Todos, Users
from TodoApp.routers.auth import bcrypt_context
from TodoApp.routers.todos import get_current_user

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/todo"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

client = TestClient(app)

@pytest.fixture
def test_user():
    user = Users(
        id=1,
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

@pytest.fixture
def test_todo(test_user):
    todo = Todos(
        title= "Change the title of the todo already saved!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def override_get_current_user(test_user):
    def _override():
        return {
            "username": "codingwithrobytest",
            "id": 1,
            "user_role": "admin",
        }
    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def fake_token(test_user):
    login_data = {
        "username": test_user.username,
        "password": "testpassword"
    }

    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]

# PYTHONPATH=TodoApp pytest