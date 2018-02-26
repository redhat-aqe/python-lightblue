"""
Custom class of BeanBag
"""

import logging

from beanbag.v2 import BeanBag, BeanBagException

LOGGER = logging.getLogger('lightblue')


class CustomBeanBag(~BeanBag):
    """
    Custom BeanBag class which prints error content
    """
    def __init__(self, *args, **kwargs):
        super(~CustomBeanBag, self).__init__(*args, **kwargs)

    def decode(self, response):
        """
        Custom decode function which prints response when request gets error
        Args:
            response (object): response from server

        Returns: response AttrDict

        """
        if response.status_code < 200 or response.status_code >= 300:
            LOGGER.warning("Invalid response code (%s) "
                           "received from service: %s",
                           response.status_code, self.base_url)
            # print response content
            raise BeanBagException(
                response, "Bad response code: %d\nResponse: %s" % (
                    response.status_code, response.content))

        return super(~CustomBeanBag, self).decode(response)
