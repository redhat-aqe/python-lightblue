import logging

LOGGER = logging.getLogger('lightblue')


class LightBlueEntity(object):
    """
    Lightblue generic entity
     - all common action for all entities are specified here
     - for specific entity create new class with this class as parent
    """
    def __init__(self,
                 lightblue_service,
                 entity_name,
                 version=None,
                 *args,
                 **kwargs):

        super(LightBlueEntity, self).__init__(*args, **kwargs)
        self.service = lightblue_service
        self.entity_name = entity_name
        self.version = version

    @staticmethod
    def check_response(response):
        """
        Check LightBlue response. It always has to contain
            {
                'status': 'COMPLETE'
                ..
            }
        Args:
            response (dict): Lightblue API response

        Returns:
             bool - True if response is with no errors / False

        """
        if response is not None and \
           'status' in response and \
           response['status'] == 'COMPLETE':
            return True
        LOGGER.error('Received invalid response from Lightblue: %s', response)
        return False

    def get_schema(self, version=None):
        """
        Get schema for generic entity
        Args:
            version (str): entity version (if missing, default is used)

        Returns:
            - dict - json schema for entity

        """
        if version is None:
            if self.version is None:
                raise ValueError("No version was provided")
            return self.service.get_schema(self.entity_name, self.version)
        else:
            return self.service.get_schema(self.entity_name, version)

    def insert_data(self, data):
        """
        Insert data to generic entity (default projection is used)
        Args:
            data (dict/list): json objects for entity

        Returns:
            - dict - lightblue response

        """
        lightblue_data = {
            'objectType': self.entity_name,
            'data': data,
            'projection': {
                'field': '*',
                'include': True,
                'recursive': True

            }
        }
        if self.version is not None:
            lightblue_data['version'] = self.version
        return self.service.insert_data(self.entity_name, self.version,
                                        lightblue_data)

    def delete_all(self):
        """
        Delete all data for generic entity
        Returns:
            - dict - lightblue response

        """
        lightblue_data = {
            'objectType': self.entity_name,
            'query': {
                'field': 'objectType',
                'op': '=',
                'rvalue': self.entity_name
            }
        }
        if self.version is not None:
            lightblue_data['version'] = self.version
        return self.service.delete_data(self.entity_name, self.version,
                                        lightblue_data)

    def delete_item(self, query):
        """
        Delete specific object according to query
        Args:
            query (dict): query for delete

        Returns:
            - dict - lightblue response

        """
        lightblue_data = {
            'objectType': self.entity_name,
            'query': query
        }
        if self.version is not None:
            lightblue_data['version'] = self.version
        return self.service.delete_data(self.entity_name, self.version,
                                        lightblue_data)

    def update_item(self, query, update):
        """
        Update specific object according to query and update field
        Args:
            query (dict): query for searching data
            update (dict): update field (new values for given fields)

        Returns:
            - dict - lightblue response

        """
        lightblue_data = {
            'objectType': self.entity_name,
            'query': query,
            'update': update
        }
        if self.version is not None:
            lightblue_data['version'] = self.version
        return self.service.update_data(self.entity_name, self.version,
                                        lightblue_data)

    def find_item(self, query, projection=None):
        """
        Find specific object according to query and projection field
        Args:
            query (dict): search query
            projection (list): specify field which will be returned
                               (default - return all)

        Returns:
            - dict - result of search query

        """
        lightblue_data = {
            'objectType': self.entity_name,
            'query': query
        }
        if self.version is not None:
            lightblue_data['version'] = self.version
        if projection is None:
            projection = {
                'field': '*',
                'include': True,
                'recursive': True
            }
        lightblue_data['projection'] = projection
        return self.service.find_data(self.entity_name, self.version,
                                      lightblue_data)

    def find_all(self, projection=None):
        """
        Find all objects of given entity
        Args:
            projection (list): custom projection (default return all items)

        Returns:
            - dict - result of search query

        """
        lightblue_data = {
            'objectType': self.entity_name,
            'query': {
                'field': 'objectType',
                'op': '=',
                'rvalue': self.entity_name
            }
        }
        if self.version is not None:
            lightblue_data['version'] = self.version
        if projection is None:
            projection = {
                'field': '*',
                'include': True,
                'recursive': True
            }
        lightblue_data['projection'] = projection
        return self.service.find_data(self.entity_name, self.version,
                                      lightblue_data)
