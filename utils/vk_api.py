import requests
from vk.exceptions import VkException
import time

class VKUtil:
    def __init__(self, token, api_version):
        self.token = token
        self.api_version = api_version

    def request_url(self, method_name, parameters, access_token=False):
        time.sleep(1)
        req_url = 'https://api.vk.com/method/{method_name}?{parameters}&v={api_v}'.format(
            method_name=method_name, api_v=self.api_version, parameters=parameters)

        if access_token:
            req_url += '&access_token={token}'.format(req_url, token=self.token)

        return req_url

    def base_info(self, id):
        fields = "universities,schools"
        r = requests.get(self.request_url('users.get', 'user_id=' + str(id) + '&fields=' + fields, access_token=True)).json()
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

    def groups(self, id):
        r = requests.get(self.request_url('groups.get',
                                          'user_id=%s&extended=1' % id, access_token=True)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']
        return r

    def photos(self, id):
        r = requests.get(self.request_url('photos.get',
                                          'user_id=%s&extended=1&album_id=profile' % id, access_token=True)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']
        return r

    def videos(self, id):
        r = requests.get(self.request_url('video.get',
                                          'owner_id=%s&extended=1' % id, access_token=True)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']
        return r

    def docs(self, id):
        r = requests.get(self.request_url('docs.get',
                                          'owner_id=%s&extended=1' % id, access_token=True)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']
        return r

    def notes(self, id):
        r = requests.get(self.request_url('notes.get',
                                          'user_id=%s&extended=1' % id, access_token=True)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']
        return r

    def subscriptions(self, id):
        r = requests.get(self.request_url('users.getSubscriptions',
                                          'user_id=%s&extended=1' % id, access_token=True)).json()
        if 'error' in r.keys():
            raise VkException('Error message: %s. Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response']
        return r