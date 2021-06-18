#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytest


@pytest.hookspec(firstresult=True)
def pytest_send_upload_request(upload_url: str, files: list, config: dict):
    """ send upload request """
