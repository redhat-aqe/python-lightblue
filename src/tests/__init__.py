try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from lightblue.service import LightBlueService


class FakeLightblueService(LightBlueService):
    def __init__(self, *args, **kwargs):
        self.data_api = Mock()
        self.metadata_api = Mock()
        self.insert_data = Mock()
        self.delete_data = Mock()
        self.update_data = Mock()
        self.find_data = Mock()
        self.get_schema = Mock()
