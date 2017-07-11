import requests
from urllib.parse import urljoin
import time
import sqlite3

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

conn = sqlite3.connect(config['tvdb']['db'])
c = conn.cursor()

class TVDB(object):
    def __init__(self):
        self.config = {}
        self.config['apikey'] = config['tvdb']['api-key']
        self.config['username'] = config['tvdb']['username']
        self.config['userkey'] = config['tvdb']['userkey']
        self.config['base_url'] = 'https://api.thetvdb.com/'
        self.config['token'] = self.get_token()

    def login(self):
        return self.api_call('post', 'login',
                           json={
                                'username': self.config['username'],
                                'userkey': self.config['userkey'],
                                'apikey': self.config['apikey']
                           })['token']

    def api_call(self, method, relative_url, **kwargs):
        headers = kwargs.pop('headers', {})

        if not relative_url == 'login':
            if self.config['token']:
             headers['Authorization'] = 'Bearer %s' % self.config['token']

        url = urljoin(self.config['base_url'], relative_url)
        response = requests.request(method, url, headers=headers, **kwargs)
        return response.json()



    def show_banners(self, show_id):
        return self.api_call('get', 'series/%d/images/query?keyType=poster' % show_id )

    def update_token(self, new_token, new_time):
        c.execute("UPDATE token SET token=?, last_token=? WHERE 1", (new_token, new_time))
        conn.commit()

    def get_token(self):
        c.execute("SELECT token,last_token FROM token")
        response = c.fetchone()
        current = time.time()

        if response[1] + 86400 < current:
            new_token = self.login()
            self.update_token(new_token, current)
            return new_token
        else:
            return response[0]
