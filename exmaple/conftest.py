pytest_plugins = 'pytester'


import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_send_upload_request(upload_url, files, config):
    from pytest_upload_report.upload_client import SignUploadClient
    client = SignUploadClient(upload_url, files)
    client.send_request(config)
    return True
