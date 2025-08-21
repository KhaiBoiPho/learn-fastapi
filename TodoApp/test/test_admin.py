from TodoApp.test.utils import *
from TodoApp.routers.admin import get_db, get_current_user
from fastapi import status
from TodoApp.models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo, override_get_current_user):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    
    # Kiểm tra dữ liệu trả về khớp với dữ liệu trong test_todo
    assert response.json() == [{
        'complete': test_todo.complete,
        'title': test_todo.title,
        'description': test_todo.description,
        'id': test_todo.id,
        'priority': test_todo.priority,
        'owner_id': test_todo.owner_id
    }]


def test_admin_delete_todo(test_todo, override_get_current_user):
    response = client.delete(f"/admin/todo/{test_todo.id}")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None


def test_admin_delete_todo_not_found(override_get_current_user):
    response = client.delete("/admin/todo/9999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}