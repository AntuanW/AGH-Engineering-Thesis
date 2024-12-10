from app.repository.topology_repository import TopologyRepository
from app.repository.device_repository import DeviceRepository


def test_each_subclass_is_singleton():
    topo_1 = TopologyRepository()
    topo_2 = TopologyRepository()
    topo_3 = TopologyRepository()
    dev_1 = DeviceRepository()
    dev_2 = DeviceRepository()

    assert topo_1 is topo_2 is topo_3
    assert dev_1 is dev_2
    assert topo_1 is not dev_1


def test_single_db_connection():
    topo_1 = TopologyRepository()
    topo_2 = TopologyRepository()
    dev_1 = DeviceRepository()

    assert topo_1.db is topo_2.db
    assert topo_1.db is dev_1.db