"""
The LighBlueService should be used as API wrapper. It makes http query based
on user's requirements.
"""

import json
import logging

from beanbag.v2 import BeanBag, POST, GET, PUT, BeanBagException

from lightblue.common import retry_session

LOGGER = logging.getLogger('lightblue')


class LightBlueService(object):
    """"
        Class for interacting with lightBlue API
    """
    def __init__(self, data_url, metadata_url, ssl_certificate=None,
                 ssl_verify=True, custom_session=None):
        self.data_url = data_url
        self.metadata_url = metadata_url
        self.ssl_certificate = ssl_certificate
        if custom_session is None:
            self.session = retry_session()
            self.session.verify = ssl_verify
            if self.ssl_certificate is not None:
                self.session.cert = self.ssl_certificate
        else:
            self.session = custom_session
        self.data_api = BeanBag(self.data_url, session=self.session,
                                use_attrdict=False)
        self.metadata_api = BeanBag(self.metadata_url,
                                    session=self.session,
                                    use_attrdict=False)

    @staticmethod
    def log_response(response):
        """
        Logging API calls response
        Args:
            response: API call response
        """

        log_response = {
            'status': response['status'],
            'matchCount': response['matchCount'],
            'modifiedCount': response['modifiedCount']
        }
        # data should be excluded from log message - include only data errors
        if response['status'] != 'COMPLETE' and 'dataErrors' in response:
            log_response['dataErrors'] = response['dataErrors']
        LOGGER.debug("%s", log_response)

    def get_schema(self, entity_name, version):
        """
        Get schema for specific entity
        Args:
            entity_name (str): entity name
            version (str): entity version

        Returns:
            - dict - schema of given entity

        """
        LOGGER.debug("%s - %s", 'GET', self.metadata_api[entity_name][version])
        return GET(self.metadata_api[entity_name][version])

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
        try:
            if version is not None:
                LOGGER.debug("%s - %s", 'PUT',
                             self.data_api.insert[entity_name][version])
                response = PUT(
                    self.data_api.insert[entity_name][version], data)
            else:
                LOGGER.debug("%s - %s", 'PUT',
                             self.data_api.insert[entity_name])
                response = PUT(self.data_api.insert[entity_name], data)

            self.log_response(response)

            return response
        except BeanBagException:
            LOGGER.exception("Insert data failed")
            LOGGER.debug(json.dumps(data))

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
        try:
            if version is not None:
                LOGGER.debug("%s - %s -%s", 'POST',
                             self.data_api.delete[entity_name][version], data)
                response = POST(
                    self.data_api.delete[entity_name][version], data)
            else:
                LOGGER.debug("%s - %s -%s", 'POST',
                             self.data_api.delete[entity_name], data)
                response = POST(self.data_api.delete[entity_name], data)

            self.log_response(response)

            return response
        except BeanBagException:
            LOGGER.exception("Delete data failed")
            LOGGER.debug(json.dumps(data))

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
        try:
            if version is not None:
                LOGGER.debug("%s - %s -%s", 'POST', self.data_api.update[
                    entity_name][version], data['query'])
                response = POST(
                    self.data_api.update[entity_name][version], data)
            else:
                LOGGER.debug("%s - %s -%s", 'POST', self.data_api.update[
                    entity_name], data['query'])
                response = POST(self.data_api.update[entity_name], data)

            self.log_response(response)

            return response
        except BeanBagException:
            LOGGER.exception("Update data failed")
            LOGGER.debug(json.dumps(data))

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
        try:
            if version is not None:
                LOGGER.debug("%s - %s -%s", 'POST',
                             self.data_api.find[entity_name][version],
                             data['query'])
                response = POST(
                    self.data_api.find[entity_name][version], data)
            else:
                LOGGER.debug("%s - %s -%s", 'POST',
                             self.data_api.find[entity_name], data['query'])
                response = POST(self.data_api.find[entity_name], data)

            self.log_response(response)

            return response
        except BeanBagException:
            LOGGER.exception("Find data failed")
            LOGGER.debug(json.dumps(data))
