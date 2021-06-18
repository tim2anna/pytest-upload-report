
English | [简体中文](index.zh.md)


pytest-upload-report is a plugin for [pytest](http://pytest.org) that upload your test report for test results.


## Features


- [x] Upload report for allure-pytest.

- [ ] Upload report for pytest-html.


## Requirements

* Python >= 3.7
* pytest
* requests
* allure-pytest, if you use allure report.
* pytest-html, if you use html report.


## Installation


You can install "pytest-upload-report" via `pip` from `PyPI`:

```shell
$ pip install pytest-upload-report
```


## Usage


### A simple example


Directly upload report files  to server by upload_url.

On the command line, add `upload_url` option when run `pytest` command:

```shell
pytest --alluredir=/tmp/my_allure_results --upload_url=http://127.0.0.1:8000/upload
```
    


### A complete example


Now let us demonstrate how to use in a vaguely real world scenario.


First, you must have a upload api on server, an example for fastapi:

```python
from typing import List
from fastapi import APIRouter, UploadFile, File, Header

router = APIRouter(prefix='/api/script', tags=['script'])

@router.post("/reports/upload")
async def report_upload_by_api(
    project_id: int,
    timestamp: int,
    username: str,
    sign: str = Header(...),
    files: List[UploadFile] = File(...),
):
    ...
    return 'ok'
```



Second, edit your conftest.py file, add `pytest_send_upload_request` hook:

```python
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_send_upload_request(upload_url, files, config):
    from pytest_upload_report.upload_client import SignUploadClient
    client = SignUploadClient(upload_url, files)
    client.send_request(config)
    return True
```

The other hooks will be blocked from executing, when then hook return `True`.
If you want to upload multiple places, don't write any return.


Third, edit pytest.init on you test project root dir:

```buildoutcfg
[pytest]
addopts = --alluredir=/tmp/my_allure_results --upload_url=http://127.0.0.1:8000/api/script/reports/upload --upload_project_id=4 --upload_username=admin --upload_secret=8FB6CFB4C8CF11EBB523DCA9048E18C3
```


Finally, run pytest command on you test project root dir:

```shell
pytest
```
    


Also, you can view source code in the example directory.


### How to Customize

If the above does not meet your needs, you can customize request client.