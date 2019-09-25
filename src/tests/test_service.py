from unittest import TestCase
import requests

from lightblue.service import LightBlueService

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


class TestLightBlueService(TestCase):
    """
    Test cases for LightBlueService class
    """

    test_docstring_prefix = "Service - "

    def shortDescription(self):  # noqa
        """Override nosetest docstrings."""
        doc = self.test_docstring_prefix + self._testMethodDoc
        return doc or None

    def setUp(self):
        self.data_url = 'http:/fake.lb.com/rest/data'
        self.metadata_url = 'http:/fake.lb.com/rest/metadata'

        self.service = LightBlueService(
            self.data_url, self.metadata_url, ssl_certificate='path/to/cert'
        )

    def test_custom_session(self):
        session = requests.session()
        service = LightBlueService(
            self.data_url,
            self.metadata_url,
            ssl_certificate='path/to/cert',
            custom_session=session,
        )
        self.assertEqual(service.session, session)

    def test_log_response_json(self):
        """
        Test response message is complete
        """
        response = Mock()
        response.json.return_value = {
            'status': 'FAILED',
            'matchCount': 0,
            'modifiedCount': 0,
            'dataErrors': None,
            'data': ['object'],
        }
        response.status_code = 200
        result = self.service.log_response(response)
        expected_result = {
            'status': 'FAILED',
            'matchCount': 0,
            'modifiedCount': 0,
            'dataErrors': None,
            'errors': None,
            'statusCode': 200,
        }
        self.assertEqual(result, expected_result)

    def test_log_response_no_json(self):
        """
        Test response message is complete - failed
        """
        response = Mock()
        response.json.side_effect = ValueError('err')
        response.text = 'response'
        response.status_code = 500
        result = self.service.log_response(response)
        expected_result = {'text_response': 'response', 'statusCode': 500}
        self.assertEqual(result, expected_result)

    @patch('requests.Session.get')
    def test_get_schema(self, mock_get):
        """
        Test of getting schema
        """
        schema = {'key': 'value'}
        mock_get.return_value.json.return_value = schema
        result = self.service.get_schema('entity', 'version')
        self.assertEqual(result, schema)

    @patch('requests.Session.put')
    def test_insert_data(self, mock_put):
        """
        Test of inserting data
        """
        data = 'object'
        resp_data = {
            'status': 'COMPLETE',
            'matchCount': 1,
            'modifiedCount': 1,
            'data': [data],
        }
        mock_put.return_value.json.return_value = resp_data
        mock_put.return_value.status_code = 200
        result = self.service.insert_data('entity', 'version', data)
        call_args = mock_put.call_args
        self.assertEqual(
            call_args[0][0], '{}/insert/entity/version'.format(self.data_url)
        )
        self.assertEqual(call_args[1], {'json': data})
        self.assertEqual(result, resp_data)

    @patch('requests.Session.put')
    def test_insert_data_failed(self, mock_put):
        """
        Test of inserting data - failed request
        """
        data = 'object'
        resp_data = {
            'status': 'FAILED',
            'matchCount': 1,
            'modifiedCount': 1,
            'data': [data],
        }
        mock_put.return_value.json.return_value = resp_data
        mock_put.return_value.status_code = 500
        result = self.service.insert_data('entity', 'version', data)
        call_args = mock_put.call_args
        self.assertEqual(
            call_args[0][0], '{}/insert/entity/version'.format(self.data_url)
        )
        self.assertEqual(call_args[1], {'json': data})
        self.assertIsNone(result)

    @patch('requests.Session.post')
    def test_delete_data(self, mock_post):
        """
        Test of deleting data
        """
        data = 'object'
        resp_data = {
            'status': 'COMPLETE',
            'matchCount': 1,
            'modifiedCount': 1,
            'data': [data],
        }
        mock_post.return_value.json.return_value = resp_data
        mock_post.return_value.status_code = 200
        result = self.service.delete_data('entity', 'version', data)
        call_args = mock_post.call_args
        self.assertEqual(
            call_args[0][0], '{}/delete/entity/version'.format(self.data_url)
        )
        self.assertEqual(call_args[1], {'json': data})
        self.assertEqual(result, resp_data)

    @patch('requests.Session.post')
    def test_delete_data_failed(self, mock_post):
        """
        Test of deleting data - failed request
        """
        data = 'object'
        resp_data = {
            'status': 'FAILED',
            'matchCount': 1,
            'modifiedCount': 1,
            'data': [data],
        }
        mock_post.return_value.json.return_value = resp_data
        mock_post.return_value.status_code = 500
        result = self.service.delete_data('entity', 'version', data)
        call_args = mock_post.call_args
        self.assertEqual(
            call_args[0][0], '{}/delete/entity/version'.format(self.data_url)
        )
        self.assertEqual(call_args[1], {'json': data})
        self.assertIsNone(result)

    @patch('requests.Session.post')
    def test_update_data(self, mock_post):
        """
        Test of updating data
        """
        data = 'object'
        resp_data = {
            'status': 'COMPLETE',
            'matchCount': 1,
            'modifiedCount': 1,
            'data': [data],
        }
        mock_post.return_value.json.return_value = resp_data
        mock_post.return_value.status_code = 200
        result = self.service.update_data('entity', 'version', data)
        call_args = mock_post.call_args
        self.assertEqual(
            call_args[0][0], '{}/update/entity/version'.format(self.data_url)
        )
        self.assertEqual(call_args[1], {'json': data})
        self.assertEqual(result, resp_data)

    @patch('requests.Session.post')
    def test_update_data_failed(self, mock_post):
        """
        Test of updating data - failed request
        """
        data = 'object'
        resp_data = {
            'status': 'FAILED',
            'matchCount': 1,
            'modifiedCount': 1,
            'data': [data],
        }
        mock_post.return_value.json.return_value = resp_data
        mock_post.return_value.status_code = 500
        result = self.service.update_data('entity', 'version', data)
        call_args = mock_post.call_args
        self.assertEqual(
            call_args[0][0], '{}/update/entity/version'.format(self.data_url)
        )
        self.assertEqual(call_args[1], {'json': data})
        self.assertIsNone(result)

    @patch('requests.Session.post')
    def test_find_data(self, mock_post):
        """
        Test of finding data
        """
        data = 'object'
        resp_data = {
            'status': 'COMPLETE',
            'matchCount': 1,
            'modifiedCount': 1,
            'data': [data],
        }
        mock_post.return_value.json.return_value = resp_data
        mock_post.return_value.status_code = 200
        result = self.service.find_data('entity', 'version', data)
        call_args = mock_post.call_args
        self.assertEqual(
            call_args[0][0], '{}/find/entity/version'.format(self.data_url)
        )
        self.assertEqual(call_args[1], {'json': data})
        self.assertEqual(result, resp_data)

    @patch('requests.Session.post')
    def test_find_data_failed(self, mock_post):
        """
        Test of finding data - failed request
        """
        data = 'object'
        resp_data = {
            'status': 'FAILED',
            'matchCount': 1,
            'modifiedCount': 1,
            'data': [data],
        }
        mock_post.return_value.json.return_value = resp_data
        mock_post.return_value.status_code = 500
        result = self.service.find_data('entity', 'version', data)
        call_args = mock_post.call_args
        self.assertEqual(
            call_args[0][0], '{}/find/entity/version'.format(self.data_url)
        )
        self.assertEqual(call_args[1], {'json': data})
        self.assertIsNone(result)
