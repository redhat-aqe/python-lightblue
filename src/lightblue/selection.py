"""LightBlueGenericSelection implementation."""

import dpath.util

from lightblue.query import LightBlueQuery


class LightBlueGenericSelection(LightBlueQuery):
    """
    Representation of an item in a collection.

    (isn't specific to any LightBlue entity)

    Attributes:
        interface (lightblue.entity.LightBlueEntity):
            wrapper to query a LightBlue method
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a LightBlueGenericSelection object.

        Args:
            interface (lightblue.entity.LightBlueEntity):
                reference to LightBlueEntity object
            *args: Description
            **kwargs: Description
        """
        self.interface = kwargs.pop('interface')

        super(LightBlueGenericSelection, self).__init__(
            self.interface, *args, **kwargs)

    def _postprocessing(self,
                        result,
                        check_response=True,
                        selector=None,
                        count=None,
                        fallback=None,
                        postprocess=None):
        """
        Post-process the response from LightBlue.

        Args:
            result (dict): response from LightBlue
            check_response (bool, optional):
                return fallback if .check_response() failed
            selector (None, optional):
                dpath selector to get the result of query
            count (None, optional):
                - matchCount have to equal count if count is int
                - matchCount < count[0] and  matchCount < count[2]
                  in case of tuple
            fallback (None, optional): value to return if any check fails
            postprocess (None, optional):
                the result will be passed as an argument to the function

        Returns:
            object:
                - whole response
                - selected part of the response
                - fallback provided to the post-process
        """
        # check response
        if check_response:
            if not self.interface.check_response(result):
                return fallback
        # check count
        if count:
            if isinstance(count, tuple):
                if result['matchCount'] < count[0]:
                    return fallback
                if len(count) > 1:
                    if result['matchCount'] > count[1]:
                        return fallback
            elif isinstance(count, int):
                if result['matchCount'] != count:
                    return fallback
        # return value (by selector) or result
        if selector:
            try:
                result = dpath.util.get(result, selector)
            except ValueError:
                result = dpath.util.values(result, selector)
        if postprocess:
            postprocess_result = postprocess(result)
            if postprocess_result is None:
                return fallback
            else:
                return postprocess_result
        else:
            return result

    def find(self, *args, **kwargs):
        """
        Postprocessing wrapper over find method.

        Args:
            *args: arguments to pass to _postprocessing()
            **kwargs: arguments to pass to _postprocessing()

        Returns:
            object: as returned by _postprocessing()
        """
        result = super(LightBlueGenericSelection, self).find()
        return self._postprocessing(result, *args, **kwargs)

    def update(self, *args, **kwargs):
        """
        Postprocessing wrapper over update method.

        Args:
            *args: arguments to pass to _postprocessing()
            **kwargs: arguments to pass to _postprocessing()

        Returns:
            object: as returned by _postprocessing()
        """
        result = super(LightBlueGenericSelection, self).update()
        return self._postprocessing(result, *args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Postprocessing wrapper over delete method.

        Args:
            *args: arguments to pass to _postprocessing()
            **kwargs: arguments to pass to _postprocessing()

        Returns:
            object: as returned by _postprocessing()
        """
        result = super(LightBlueGenericSelection, self).delete()
        return self._postprocessing(result, *args, **kwargs)

    # .insert() method is public, without any changes

    @staticmethod
    def get_selector_query(data, primary_keys):
        """
        Get a query to identify an entity.

        This method receives an item and PKs and returns a query.

        Q: Why this method is static if we have PKs in constructor?
        A: This method have to be accessible from the classmethod
        insert_and_select(), which has no access to the attribute.

        Q: Why PKs are not class attributes?
        A: Even if we will define PKs as a class attribute and
        override them in child class - overridden value won't be
        accessible from the classmethod.

        Args:
            data (dict): data as stored in LightBlue
            primary_keys (dict):
                - key is a filed name
                - value is dpath selector

        Returns:
            list: query (as pairs) to identify a specific entity.
        """
        query = []
        for key, selector in primary_keys.iteritems():
            query.append((key, dpath.util.get(data, selector), ))
        return query

    # TODO: design a classmethod to insert item and return selector

    # .add_raw_query() method is public from LightBlueQuery

    def filter_created_by(self, service):
        """
        Select items created by specific service.

        Args:
            service (str): service name

        Allows method chaining, returns self.
        """
        self._add_to_query(createdBy=service)
        return self

    @property
    def first(self):
        """
        Get the first element of response for a query.

        Returns:
            (dict, None):
                first item if available, None otherwise
        """
        return self.find(
            count=(1, ),
            selector='/processed/0',
            fallback=None)

    @property
    def exist(self):
        """
        Check if items are available for the query.

        Returns:
            bool: True if items exist, False otherwise
        """
        result = self.find()
        if result is None:
            return False
        else:
            return result['matchCount'] > 0

    @property
    def all(self):
        """
        Get all elements of response for given quert

        Returns:
            (list / []) - list of found items, empty list otherwise

        """
        return self.find(
            count=(1, ),
            selector='/processed',
            fallback=[]
        )
