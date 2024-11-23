from app.repository.connection_repository import ConnectionRepository
from app.models.connection import ConnectionModel

def test_basic_connection():
    repo = ConnectionRepository()
    repo.get_collection()

def test_find_all():
    repo = ConnectionRepository()
    connections = repo.find_all()
    print(connections)
    assert len(connections) == 1
    assert type(connections[0]) is ConnectionModel