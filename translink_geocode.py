import requests

API_URL = "http://api.translink.ca"

def _get(api_key, endpoint, params=None):
    return requests.get(API_URL + "/rttiapi/v1/" + endpoint,
                        params=dict({"apikey": api_key},
                                    **params)).json()

def get_stop(api_key, stop_id, params=None):
    return _get(api_key, "stops/" + stop_id, params=params)
