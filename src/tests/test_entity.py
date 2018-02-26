from unittest import TestCase

from lightblue.entity import LightBlueEntity
from . import FakeLightblueService


class TestLightBlueEntity(TestCase):
    """
    Test cases for LightBlueEntity class
    """
    test_docstring_prefix = "Generic entity - "

    def shortDescription(self):  # noqa
        """Override nosetest docstrings."""
        doc = self.test_docstring_prefix + self._testMethodDoc
        return doc or None

    def setUp(self):
        self.fake_lightblue_service = FakeLightblueService()
        self.lb_entity = LightBlueEntity(self.fake_lightblue_service,
                                         'fake-name', 'fake_version')

    def test_check_response_success(self):
        """
        Test response message is complete
        """
        response = {
            'status': 'COMPLETE'
        }
        result = self.lb_entity.check_response(response)
        self.assertTrue(result)

    def test_check_response_failure(self):
        """
        Test response message is missing some values
        """
        result = self.lb_entity.check_response(None)
        self.assertFalse(result)

        # no status in response
        response = {
            'fake-key': 'value'
        }
        result = self.lb_entity.check_response(response)
        self.assertFalse(result)

        # status is not equal to COMPLETE
        response = {
            'status': 'PARTIAL'
        }
        result = self.lb_entity.check_response(response)
        self.assertFalse(result)

    def test_get_schema_no_version(self):
        """
        Test get entity schema - no version provided
        """
        self.lb_entity.version = None
        with self.assertRaises(ValueError):
            self.lb_entity.get_schema()

    def test_get_schema_class_version(self):
        """
        Test get entity schema - class version used
        """
        self.lb_entity.get_schema()
        self.fake_lightblue_service.get_schema.assert_called_once_with(
            self.lb_entity.entity_name, self.lb_entity.version
        )

    def test_get_schema_given_version(self):
        """
        Test get entity schema - arg version used
        """
        self.lb_entity.get_schema('my_version')
        self.fake_lightblue_service.get_schema.assert_called_once_with(
            self.lb_entity.entity_name, 'my_version'
        )

    def test_insert_data(self):
        """
        Test insert new data
        """
        expected_data = {
            'objectType': self.lb_entity.entity_name,
            'data': 'fake_data',
            'version': self.lb_entity.version,
            'projection': {
                'field': '*',
                'include': True,
                'recursive': True
            }
        }
        self.lb_entity.insert_data('fake_data')
        self.fake_lightblue_service.insert_data.assert_called_once_with(
            self.lb_entity.entity_name, self.lb_entity.version, expected_data
        )

    def test_delete_all(self):
        """
        Test delete all documents
        """
        expected_data = {
            'objectType': self.lb_entity.entity_name,
            'version': self.lb_entity.version,
            'query': {
                'field': 'objectType',
                'op': '=',
                'rvalue': self.lb_entity.entity_name
            }
        }
        self.lb_entity.delete_all()
        self.fake_lightblue_service.delete_data.assert_called_once_with(
            self.lb_entity.entity_name, self.lb_entity.version, expected_data
        )

    def test_delete_item(self):
        """
        Test delete document based on query
        """
        query = 'fake_query'
        expected_data = {
            'objectType': self.lb_entity.entity_name,
            'version': self.lb_entity.version,
            'query': query
        }
        self.lb_entity.delete_item(query)
        self.fake_lightblue_service.delete_data.assert_called_once_with(
            self.lb_entity.entity_name, self.lb_entity.version, expected_data
        )

    def test_update_item(self):
        """
        Test update document based on query and given data
        """
        query = 'fake_query'
        data = 'fake_data'
        expected_data = {
            'objectType': self.lb_entity.entity_name,
            'version': self.lb_entity.version,
            'query': query,
            'update': data
        }
        self.lb_entity.update_item(query, data)
        self.fake_lightblue_service.update_data.assert_called_once_with(
            self.lb_entity.entity_name, self.lb_entity.version, expected_data
        )

    def test_find_item(self):
        """
        Test find document based on query
        """
        query = 'fake_query'
        expected_data = {
            'objectType': self.lb_entity.entity_name,
            'version': self.lb_entity.version,
            'query': query,
            'projection': {
                'field': '*',
                'include': True,
                'recursive': True
            }
        }
        self.lb_entity.find_item(query)
        self.fake_lightblue_service.find_data.assert_called_once_with(
            self.lb_entity.entity_name, self.lb_entity.version, expected_data
        )

    def test_find_all(self):
        """
        Test find all documents
        """
        query = {
            'field': 'objectType',
            'op': '=',
            'rvalue': self.lb_entity.entity_name
        }
        expected_data = {
            'objectType': self.lb_entity.entity_name,
            'version': self.lb_entity.version,
            'query': query,
            'projection': {
                'field': '*',
                'include': True,
                'recursive': True
            }
        }
        self.lb_entity.find_all()
        self.fake_lightblue_service.find_data.assert_called_once_with(
            self.lb_entity.entity_name, self.lb_entity.version, expected_data
        )
