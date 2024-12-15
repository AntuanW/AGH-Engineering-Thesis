from abc import abstractmethod, ABC


class Parser(ABC):

    def __init__(self, source):
        self.source = source
        self.data = None

    @abstractmethod
    def _read_data(self):
        raise NotImplementedError()

    @abstractmethod
    def _parse(self):
        raise NotImplementedError()

    def _get_results(self):
        return self.data

    @classmethod
    def from_source(cls, source):
        instance = cls(source)
        instance._read_data()
        instance._parse()
        return instance._get_results()
