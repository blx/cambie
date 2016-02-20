from .prelude import merge

import requests

API_URL = "http://api.translink.ca/rttiapi/v1/"

def _get(api_key, endpoint, params=None):
    return requests.get(API_URL + endpoint,
                        headers={"Accept": "application/JSON"},
                        params=merge({'apikey': api_key},
                                     params)).json()

def get_stop(api_key, stop_id, params=None):
    "Returns dict of info about the stop with 5-digit stop_id."
    return _get(api_key, "stops/" + stop_id, params)
