import requests
from vk.exceptions import VkException
import time


class VKUtil:
    def __init__(self, token, api_version):
        self.token = token
        self.api_version = api_version

    def request_url(self, method_name, parameters, access_token=False):
        time.sleep(0.2)
        req_url = 'https://api.vk.com/method/{method_name}?{parameters}&v={api_v}'.format(
            method_name=method_name, api_v=self.api_version, parameters=parameters)

        if access_token:
            req_url += '&access_token={token}'.format(req_url, token=self.token)

        return req_url

    def base_info(self, id):
        fields = "universities,schools,country,city,sex,books,bdate,activities,about,career,schools," \
                 "photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig," \
                 "military"
        r = requests.get(self.request_url('users.get', 'user_id=' + str(id) + '&fields=' + fields,
                                          access_token=True)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']
        return r

    def friends(self, id):
        r = requests.get(self.request_url('friends.get',
                                          'user_id=%s&fields=uid,first_name,last_name,photo' % id)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']
        return r

    def get_subscriptions(self, id):
        r = requests.get(self.request_url('users.getSubscriptions', 'user_id=' + str(id) + "&extended=1",
                                          access_token=True)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']["items"]
        return r
