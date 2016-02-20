import re
import urllib
import requests

def find_input(html, k):
    """Returns the value of the hidden input field `k` in `html`."""
    m = re.search(r'id="%s" value="([^"]*)"' % k,
                  html)
    return m.group(1) if m else ''

def login(email, password):
    endpoint = 'https://www.compasscard.ca/SignIn'
    headers = {
        'Referer': 'https://www.compasscard.ca/SignIn',
        'Origin': 'https://www.compasscard.ca',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
    }

    r = requests.get(endpoint)
    cookies = r.cookies

    form = {k: find_input(r.text, k)
            for k in ('__CSRFTOKEN', '__VIEWSTATE', '__VIEWSTATEGENERATOR',
                      '__EVENTVALIDATION')}

    form = dict(form, **{
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$txtSignInEmail': '',
        'ctl00$txtSignInPassword': '',
        'ctl00$Content$emailInfo$txtEmail': email,
        'ctl00$Content$passwordInfo$txtPassword': password,
        'ctl00$Content$passwordInfo$email': '',
        'ctl00$Content$btnSignIn': 'Sign in'
    })

    r = requests.post(endpoint,
                      headers=headers,
                      cookies=cookies,
                      data=form)
    return r

def get_csv(ccsn, start, end):
    csv_endpoint = 'https://www.compasscard.ca/handlers/cardhistorypdf.ashx?ccsn=01640753831658241285'
    params = {
        'type': 2,
        'csv': 'true'
    }

    format_date = lambda dt: dt.strftime('%d/%m/%Y %I:%M:%S %p')

    # Compass card site needs spaces in URL params to be "%20", not requests'
    # default of "+".
    format_params = lambda d: '&'.join('%s=%s' % (k, urllib.quote(str(v)))
                                       for k, v in d.iteritems())

    return requests.get(csv_endpoint,
                        params=format_params(dict(params,
                                                  start=format_date(start),
                                                  end=format_date(end),
                                                  ccsn=ccsn))).text
