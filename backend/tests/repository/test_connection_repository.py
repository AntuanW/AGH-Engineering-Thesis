from app.repository.connection_repository import ConnectionRepository


def test_basic_connection():
    repo = ConnectionRepository()
    repo.get_collection()
