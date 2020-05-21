"""
The LighBlueService should be used as API wrapper. It makes http query based
on user's requirements.
"""

import json
import logging

from lightblue.common import retry_session

LOGGER = logging.getLogger('lightblue')


class LightBlueService(object):
    """"
        Class for interacting with lightBlue API
    """

    def __init__(
        self,
        data_url,
        metadata_url,
        ssl_certificate=None,
        ssl_verify=True,
        custom_session=None,
    ):
        self.data_url = data_url.rstrip('/')
        self.metadata_url = metadata_url.rstrip('/')
        self.ssl_certificate = ssl_certificate
        if custom_session is None:
            self.session = retry_session()
            self.session.verify = ssl_verify
            if self.ssl_certificate is not None:
                self.session.cert = self.ssl_certificate
        else:
            self.session = custom_session

    @staticmethod
    def log_response(response):
        """
        Logging API calls response
        Args:
            response: API call response
        """
        log_response = {
            'statusCode': response.status_code,
            'elapsed': response.elapsed.total_seconds()
        }
        try:
            response_data = response.json()
            log_response['status'] = response_data.get('status')
            log_response['matchCount'] = response_data.get('matchCount')
            log_response['modifiedCount'] = response_data.get('modifiedCount')
            # data should be excluded from log message - include only
            # data errors
            if response_data.get('status') != 'COMPLETE':
                log_response['dataErrors'] = response_data.get('dataErrors')
                log_response['errors'] = response_data.get('errors')
        except ValueError:
            log_response['text_response'] = response.text

        LOGGER.debug("LightBlue response - %s",
                     log_response, extra=log_response)
        return log_response

    def get_schema(self, entity_name, version):
        """
        Get schema for specific entity
        Args:
            entity_name (str): entity name
            version (str): entity version

        Returns:
            - dict - schema of given entity

        """
        url = '{metadata_url}/{entity_name}/{version}'.format(
            metadata_url=self.metadata_url,
            entity_name=entity_name,
            version=version
        )
        LOGGER.debug("%s - %s", 'GET', url)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def insert_data(self, entity_name, version, data):
        """
        Insert request
        Args:
            entity_name (str): entity name
            version (str/None): entity version
            data (dict/list): new lightblue documents

        Returns:
            - dict - lightblue response

        """
        url = '{data_url}/insert/{entity_name}'
        if version is not None:
            url = url + '/{version}'
        url = url.format(
            data_url=self.data_url, entity_name=entity_name, version=version
        )
        LOGGER.debug("%s - %s", 'PUT', url)
        response = self.session.put(url, json=data)
        self.log_response(response)
        if response.status_code != 200:
            LOGGER.error('Insert data failed - %s', json.dumps(data))
            return None
        return response.json()

    def delete_data(self, entity_name, version, data):
        """
        Delete data according to data query
        Args:
            entity_name (str): entity name
            version (str/None): entity version
            data (dict): data contains query

        Returns:
            - dict - lightblue response

        """

        url = '{data_url}/delete/{entity_name}'
        if version is not None:
            url = url + '/{version}'
        url = url.format(
            data_url=self.data_url, entity_name=entity_name, version=version
        )
        LOGGER.debug("%s - %s", 'POST', url)
        response = self.session.post(url, json=data)
        self.log_response(response)
        if response.status_code != 200:
            LOGGER.error('Delete data failed - %s', json.dumps(data))
            return None
        return response.json()

    def update_data(self, entity_name, version, data):
        """
        Update data according to data query and update field
        Args:
            entity_name (str): entity_name
            version (str/None): entity version
            data (dict): data contains query and update field

        Returns:
            - dict - lightblue response

        """
        url = '{data_url}/update/{entity_name}'
        if version is not None:
            url = url + '/{version}'
        url = url.format(
            data_url=self.data_url, entity_name=entity_name, version=version
        )
        LOGGER.debug("%s - %s", 'POST', url)
        response = self.session.post(url, json=data)
        self.log_response(response)
        if response.status_code != 200:
            LOGGER.error('Update data failed - %s', json.dumps(data))
            return None
        return response.json()

    def find_data(self, entity_name, version, data):
        """
        Find data according to data query
        Args:
            entity_name (str): entity name
            version (str/None): entity version
            data (dict): data contains query and projection field

        Returns:
            - dict - result of search and projection query

        """

        url = '{data_url}/find/{entity_name}'
        if version is not None:
            url = url + '/{version}'
        url = url.format(
            data_url=self.data_url, entity_name=entity_name, version=version
        )
        LOGGER.debug("%s - %s", 'POST', url)
        response = self.session.post(url, json=data)
        self.log_response(response)
        if response.status_code != 200:
            LOGGER.error('Find data failed - %s', json.dumps(data))
            return None
        return response.json()
