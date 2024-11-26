from app.repository.connection_repository import ConnectionRepository
from app.models.connection import ConnectionModel

class TestConnectionRepository:
    def test_basic_connection(self):
        repo = ConnectionRepository()
        repo.get_collection()

    def test_find_all(self):
        repo = ConnectionRepository()
        connection = ConnectionModel(
            device1="dev1",
            interface1="int1",
            device2="dev2",
            interface2="int2"
        )
        conn_id = repo.insert(connection)

        connections = repo.find_all()

        try:
            assert len(connections) > 0
            assert type(connections[0]) is ConnectionModel
        finally:
            assert repo.delete_one({"_id": conn_id}) == 1