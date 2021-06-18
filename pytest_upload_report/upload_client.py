import requests
import time
from hashlib import md5


class UploadClient(object):
    def __init__(self, upload_url, files):
        self.upload_url = upload_url
        self.files = files

    def send_request(self, data=None, _json=None, params={}, headers={}):
        multiple_files = []
        for _file in self.files:
            multiple_files.append(('files', open(_file, 'rb'), ))
        return requests.post(
            self.upload_url,
            data=data,
            json=_json,
            params=params,
            files=multiple_files,
            headers=headers
        )


class SignUploadClient(UploadClient):
    def send_request(self, config={}):
        params = {  # noqa
            'project_id': config.get('upload_project_id', ''),
            'timestamp': str(int(time.time())),
            'username': config.get('upload_username', '')
        }
        hash_str = f'project_id={params["project_id"]}&timestamp={params["timestamp"]}&username={params["username"]}'
        secret = config.get('upload_secret', '')
        sign = md5((hash_str + secret).encode('utf-8')).hexdigest().upper()
        headers = {'sign': sign}
        response = super().send_request(params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(response.text)
