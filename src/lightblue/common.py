import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def retry_session(session=None):
    """
    Retry session in case it failed
    More info: https://github.com/mikem23/keepalive-race

    Args:
        session (object): already created session - in case it is missing new
        session is created
    Returns:
        session object with retry settings
    """
    if not session:
        session = requests.Session()
    retry = Retry(
        total=5,
        read=5,
        connect=5,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
