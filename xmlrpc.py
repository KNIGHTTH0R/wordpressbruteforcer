# WordpressScanner takes care of the login (tries) to WP
# for now, it's using xmlrpc login only, standard wp login
# might be added as well

# proxy support
# timeout support
import requests as req
from config import XMLRPC_POST_DATA

class Xmlrpc:
    def __init__(self, url, username, password, user_agent, proxy=None, timeout=None):
        self._url = url
        self._username = username
        self._password = password
        self._user_agent = user_agent

        if proxy:
            self._proxy = proxy
        else:
            self._proxy = None

        if timeout:
            self._timeout = timeout
        else:
            self._timeout = 30


    # checks if user and password are valid
    def check_credentials(self):
        headers = {'Content-Type':'application/xml',
                   'User-Agent':self._user_agent}
        url = '{}/xmlrpc.php'.format(self._url)
        xml_data = XMLRPC_POST_DATA.strip().replace('{USERNAME}', self._username)
        xml_data = xml_data.replace('{PASSWORD}', self._password)
        if self._proxy:
            resp = req.post(url, data=xml_data, headers=headers, proxies=self._proxy, timeout=self._timeout, verify=False)
        else:
            resp = req.post(url, data=xml_data, headers=headers, timeout=self._timeout, verify=False)

        if 'blogid' in resp.text:
            return [resp.status_code, len(resp.text), True]
        else:
            return [resp.status_code, len(resp.text), False]


    # check if xmlrpc is enabled
    @staticmethod
    def test_xmlrpc(url, proxy):
        headers = {'Content-Type': 'application/xml',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}
        url = '{}/xmlrpc.php'.format(url)
        xml_data = XMLRPC_POST_DATA.strip().replace('{USERNAME}', 'canna')
        xml_data = xml_data.replace('{PASSWORD}','htraetalf')
        if proxy:
            resp = req.post(url, data=xml_data, headers=headers, proxies=proxy, verify=False)
        else:
            resp = req.post(url, data=xml_data, headers=headers, verify=False)

        return '<int>403</int>' in resp.text

