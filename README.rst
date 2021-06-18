====================
pytest-upload-report
====================

.. image:: https://img.shields.io/pypi/v/pytest-upload-report.svg
    :target: https://pypi.org/project/pytest-upload-report
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-upload-report.svg
    :target: https://pypi.org/project/pytest-upload-report
    :alt: Python versions

.. image:: https://travis-ci.org/tim2anna/pytest-upload-report.svg?branch=master
    :target: https://travis-ci.org/tim2anna/pytest-upload-report
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/tim2anna/pytest-upload-report?branch=master
    :target: https://ci.appveyor.com/project/tim2anna/pytest-upload-report/branch/master
    :alt: See Build Status on AppVeyor


English | `简体中文 <docs/index.zh.md>`_


pytest-upload-report is a plugin for `pytest`_ that upload your test report for test results.


Features
--------

* Upload report for allure-pytest.
* Upload report for pytest-html.


Requirements
------------

* Python >= 3.7
* pytest
* requests
* allure-pytest, if you use allure report.
* pytest-html, if you use html report.


Installation
------------

You can install "pytest-upload-report" via `pip`_ from `PyPI`_::

    $ pip install pytest-upload-report


Usage
-----

A simple example
^^^^^^^^^^^^^^^^

Directly upload report files  to server by upload_url.

On the command line, add `upload_url` option when run `pytest` command::

    pytest --alluredir=/tmp/my_allure_results --upload_url=http://127.0.0.1:8000/upload


A complete example
^^^^^^^^^^^^^^^^^^^

Now let us demonstrate how to use in a vaguely real world scenario.


First, you must have a upload api on server, an example for fastapi::

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


Second, edit your conftest.py file, add `pytest_send_upload_request` hook::

    import pytest

    @pytest.hookimpl(tryfirst=True)
    def pytest_send_upload_request(upload_url, files, config):
        from pytest_upload_report.upload_client import SignUploadClient
        client = SignUploadClient(upload_url, files)
        client.send_request(config)
        return True

The other hooks will be blocked from executing, when then hook return `True`.
If you want to upload multiple places, don't write any return.


Third, edit pytest.init on you test project root dir::

    [pytest]
    addopts = --alluredir=/tmp/my_allure_results --upload_url=http://127.0.0.1:8000/api/script/reports/upload --upload_project_id=4 --upload_username=admin --upload_secret=8FB6CFB4C8CF11EBB523DCA9048E18C3


Finally, run pytest command on you test project root dir::

    $ pytest


Also, you can view source code in the example directory.


How to Customize
^^^^^^^^^^^^^^^^^

If the above does not meet your needs, you can customize request client.



Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-upload-report" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/tim2anna/pytest-upload-report/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
