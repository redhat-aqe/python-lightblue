"""LightBlueQuery implementation."""


class IncompleteQuery(Exception):
    """Attempt to execute a query to LightBlue (w/o proper data)."""

    pass


class LockedQuery(Exception):
    """Attempt to execute non-find query to LightBlue second+ time."""

    pass


class LightBlueQuery(object):
    """
    LightBlue query representation.

    (in both executed and non-executed state)

    Attributes:
        interface (lightblue.entity.LightBlueEntity):
            wrapper to query a LightBlue method
    """

    def __init__(self,
                 interface,
                 *args, **kwargs):
        """
        Initialize a LightBlueQuery object.

        Args:
            interface (lightblue.entity.LightBlueEntity):
                reference to LightBlueEntity object,
                created in collection class
                (to avoid session creation on each initialization)
            *args: list of pairs/triples with initial query
            **kwargs: dict with initial query (equals)
        """
        super(LightBlueQuery, self).__init__()
        # lock to avoid calling multiple times
        self._locked = False
        # setup interface to LB
        self.interface = interface
        # query is a list of triples (field, op, rvalue)
        queries_pairs = self._kwargs_to_pairs(**kwargs)
        args = map(self._query_pairs_to_triples, args)
        queries_pairs = map(self._query_pairs_to_triples, queries_pairs)
        self._queries = args + queries_pairs
        self._raw_queries = []
        # projections is a list of fields
        self._projections = []
        # projections_recursive is a list of fields with recursive=True
        self._projections_recursive = []
        # update set is a key-value dict
        self._update_set = {}
        # update unset is a fields list
        self._update_unset = []
        # update append is a dict
        self._update_append = {}

    @property
    def kwargs_aliases(self):
        """
        Return aliases for LightBlue fields.

        It is better to override them in child class, than pass
        another keyword argument and mix it with kwargs.

        Returns:
            dict: empty dict, no aliases by default
        """
        return {}

    # helper methods to parse args
    @staticmethod
    def _query_pairs_to_triples(query):
        """
        Transform pairs (no changes in case of triples).

        Skips triples by default.

        Args:
            query (tuple): pair (field, rvalue)
                or triple (field, relation, rvalue)

        Returns:
            tuple: triple (field, relation, rvalue)
        """
        if len(query) == 3:
            return query
        else:
            return query[0], '=', query[1]

    def _kwargs_to_pairs(self, **kwargs):
        """
        Transform kwargs to pairs.

        Args:
            **kwargs: query values

        Returns:
            tuple: (field, rvalue)
        """
        pairs = []
        for key, value in kwargs.iteritems():
            if key in self.kwargs_aliases:
                pairs.append((self.kwargs_aliases[key], value, ))
            else:
                pairs.append((key, value, ))
        return pairs

    # internal methods to update query/projection/update
    def _add_to_query(self, *args, **kwargs):
        """
        Transform and save query into the attribute.

        Args:
            *args: list of pairs/triples with query
            **kwargs: dict with query (equals)
        """
        queries_pairs = self._kwargs_to_pairs(**kwargs)
        args = map(self._query_pairs_to_triples, args)
        queries_pairs = map(self._query_pairs_to_triples, queries_pairs)
        self._queries += args + queries_pairs

    def add_raw_query(self, query):
        """
        Save raw query to the attribute.

        This is a public method, because query can be constructed
        on the abstraction level of a collection.

        Args:
            query (dict): raw LightBlue query
        """
        self._raw_queries.append(query)

    def _add_to_projection(self, *args, **kwargs):
        """
        Transform and save projection into the attribute.

        Args:
            *args: field names
            **kwargs: dict with recursive key (fields with recursive=True)
        """
        recursive = kwargs.pop('recursive', [])
        self._projections += list(args)
        self._projections_recursive += recursive

    def _add_to_update(self,
                       _set=None,
                       unset=None,
                       append=None):
        """
        Save update data to the attribute.

        Args:
            _set (dict, optional):  part of the update query
            unset (list, optional):  part of the update query
            append (dict, optional):  part of the update query
        """
        if _set is not None:
            self._update_set.update(_set)
        if unset is not None:
            self._update_unset += unset
        if append is not None:
            self._update_append.update(append)

    def _refresh(self):
        """
        Clear projection and update.

        Leaves query as is.
        """
        self._projections = []
        self._projections_recursive = []
        self._update_set = {}
        self._update_unset = []
        self._update_append = {}
        # unlock future queries
        self._locked = False

    @staticmethod
    def _and(*args):
        """
        Logical AND for multiple queries.

        Args:
            *args: list of queries

        Returns:
            dict: LightBlue query
        """
        return {
            "$and": list(args)
        }

    # properties, that construct a request
    @property
    def _has_query(self):
        """
        Object has at least one query specified.

        Returns:
            bool: True if has, False otherwise
        """
        return len(self._queries) > 0 or \
            len(self._raw_queries) > 0

    @property
    def _query(self):
        """
        Construct LightBlue query.

        Returns:
            dict: LightBlue query
        """
        dict_queries = [{
            'field': query[0],
            'op': query[1],
            'rvalue': query[2]
        } for query in self._queries]
        return self._and(*(dict_queries + self._raw_queries))

    @property
    def _has_projection(self):
        """
        Object has at least one projection specified.

        Returns:
            bool: True if has, False otherwise
        """
        return len(self._projections) > 0 or \
            len(self._projections_recursive) > 0

    @property
    def _projection(self):
        """
        Construct LightBlue projection.

        Returns:
            dict: LightBlue projection
        """
        normal = [{
            'field': field,
            'include': True
        } for field in self._projections]
        recursive = [{
            'field': field,
            'include': True,
            'recursive': True
        } for field in self._projections_recursive]
        return normal + recursive

    @property
    def _has_update(self):
        """
        Object has at least one update specified.

        Returns:
            bool: True if has, False otherwise
        """
        return bool(self._update_set) or \
            len(self._update_unset) > 0 or \
            bool(self._update_append)

    @property
    def _update(self):
        """
        Construct LightBlue update.

        Returns:
            dict: LightBlue update
        """
        result = {}
        if self._update_set:
            result['$set'] = self._update_set
        if self._update_unset:
            result['$unset'] = self._update_unset
        if self._update_append:
            result['$append'] = self._update_append
        return result

    def find(self):
        """
        Execute find call to LightBlue.

        Returns: raw response from LB
        """
        if self._has_query:
            if self._has_projection:
                return self.interface.find_item(
                    self._query,
                    projection=self._projection)
            else:
                return self.interface.find_item(self._query)
        else:
            if self._has_projection:
                return self.interface.find_all(
                    projection=self._projection)
            else:
                return self.interface.find_all()

    def update(self):
        """
        Execute update call to LightBlue.

        Returns: raw response from LB

        Raises:
            IncompleteQuery: in case of unspecified update
            LockedQuery: in case of second+ call
        """
        if self._locked:
            raise LockedQuery()
        if self._has_query and self._has_update:
            self._locked = True
            return self.interface.update_item(
                self._query, self._update)
        else:
            raise IncompleteQuery()

    def delete(self):
        """
        Execute delete call to LightBlue.

        Returns:
            object: raw response from LB

        Raises:
            IncompleteQuery: in case of unspecified query
                (can't delete all items by default)
            LockedQuery: in case of second+ call
        """
        if self._locked:
            raise LockedQuery()
        if self._has_query:
            self._locked = True
            return self.interface.delete_item(self._query)
        else:
            raise IncompleteQuery()

    @staticmethod
    def insert(data, interface):
        """
        Insert a new item to the collection.

        Args:
            data (dict): data as required by a schema
            interface (metaxor.lightblue.base.LightBlueEntity):
                wrapper to query LightBlue methods

        Returns:
            dict: raw response from LB
        """
        return interface.insert_data(data)
