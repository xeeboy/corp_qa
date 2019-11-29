# -*- coding: utf-8 -*-

import requests

AppID = '17436578'
API_Key = 'wvS2o1QHFVXV9ezQK4VcBaZp'
Secret_Key = 'pd7jZCy19L2AYCInNoghuNgZGoTIzKFT'


class BdOCR:
    """
    Get BaiDu-API to run ocr-tec
    """
    def __init__(self, app_id, api_key, secret_key):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.token = self._get_token()

    def _get_token(self):
        base_url = 'https://aip.baidubce.com/oauth/2.0/token?'
        url = base_url + ('grant_type=client_credentials&client_id={}'
                          '&client_secret={}'.format(self.api_key,
                                                     self.secret_key))
        r = requests.post(url)
        js = r.json()
        return js['access_token']

    def read_words(self, img_url):
        base_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token='
        url = base_url + self.token
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'url': img_url}
        r = requests.post(url, headers=headers, data=data)
        js = r.json()
        try:
            return js['words_result']
        except KeyError:
            return []
