import json
import urllib2
import uuid

from .utils import normalised_url

class RhodecodeClientError(Exception):
    pass

class RhodecodeClient(object):
    def __init__(self, rhodecode_url, api_key):
        self._rhodecode_url = rhodecode_url
        self._api_key = api_key

    def rhodecode_url(self):
        return self._rhodecode_url

    def api_key(self):
        return self._api_key

    def api_url(self):
        return normalised_url("/".join((self.rhodecode_url(), "_admin/api")))

    def request_data(self, method_name):
        return {'id' : self.next_request_id(), 'api_key': self.api_key(), 
            'method':method_name, 'args': {}
        }

    def request(self):
        request = urllib2.Request(self.api_url())
        request.add_header('content-type', 'text/plain')
        return request

    def get_response(self, request_data):
        return urllib2.urlopen(self.request(), json.dumps(request_data))

    def send_request(self, request_data):
        response_data = self.get_response(request_data).readlines()
        if not response_data:
            raise RhodecodeClientError("No data in response from rhodecode server {}".format(self.rhodecode_url()))
        response_data = json.loads(response_data[0])
        self.check_response_data_for_error(response_data)
        self.check_response_data_id(request_data, response_data)
        return response_data['result']

    def check_response_data_for_error(self, response_data):
        response_error = response_data['error']
        if response_error:
            raise RhodecodeClientError('Rhodecode server {} returned error: {}'.format(self.rhodecode_url(), response_error))

    def check_response_data_id(self, request_data, response_data):
        request_id = request_data['id']
        response_id = response_data['id'] 
        if response_id != request_id:
            raise RhodecodeClientError('Rhodecode server {} sent response with id {}, but request id was {}'.format(self.rhodecode_url(), response_id, request_id))

    def next_request_id(self):
        return str(uuid.uuid1())

    def get_repos(self):
        return self.send_request(self.request_data('get_repos'))
        

