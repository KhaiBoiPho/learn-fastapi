from TodoApp.routers.todos import get_db
from fastapi import status
from TodoApp.models import Todos
from TodoApp.test.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo, override_get_current_user):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': test_todo.complete, 
                                'title': test_todo.title,
                                'description': test_todo.description,
                                'id': test_todo.id,
                                'priority': test_todo.priority, 
                                'owner_id': test_todo.owner_id
                                }]


def test_read_one_authenticated(test_todo, override_get_current_user):
    response = client.get(f"/todos/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': test_todo.complete, 
                                'title': test_todo.title,
                                'description': test_todo.description,
                                'id': test_todo.id,
                                'priority': test_todo.priority, 
                                'owner_id': test_todo.owner_id
                                }


def test_read_one_authenticated_not_found(override_get_current_user):
    response = client.get("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_todo(test_todo, fake_token):
    request_data={
        'title': test_todo.title,
        'description': test_todo.description,
        'priority': test_todo.priority,
        'complete': test_todo.complete,
        'owner_id': test_todo.owner_id,
    }

    headers = {"Authorization": f"Bearer {fake_token}"}
    response = client.post('/todos/todo/', json=request_data, headers=headers)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(test_todo, fake_token):
    request_data={
        'title': test_todo.title,
        'description': test_todo.description,
        'priority': test_todo.priority,
        'complete': test_todo.complete,
        'owner_id': test_todo.owner_id,
    }

    headers = {"Authorization": f"Bearer {fake_token}"}
    response = client.put(f'/todos/todo/{test_todo.id}', json=request_data, headers=headers)
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model.title == test_todo.title


def test_update_todo_not_found(test_todo, override_get_current_user):
    request_data={
        'title':'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todos/todo/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo, override_get_current_user):
    response = client.delete(f'/todos/todo/{test_todo.id}')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None


def test_delete_todo_not_found(test_todo, override_get_current_user):
    response = client.delete('/todos/todo/9996756756') 
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}