
简体中文 | [English](index.md)


pytest-upload-report是用于上传pytest测试报告文件的一款插件。


## 特性


- [x] 上传allure-pytest报告

- [ ] 上传pytest-html报告


## 必须条件

* Python >= 3.7
* pytest
* requests
* allure-pytest(可选，如果你想上传allure报告时必须安装)
* pytest-html(可选，如果你想上传html报告时必须安装)


## 安装

通过pip命令安装

```shell
$ pip install pytest-upload-report
```


## 使用


### 简单例子


直接上传报告文件到服务器，在运行pytest命令时加上`upload_url`参数即可：

```shell
pytest --alluredir=/tmp/my_allure_results --upload_url=http://127.0.0.1:8000/upload
```
    


### 复杂例子

下面是一个真实应用的例子。


1. 首先你必须准备一个上传文件的接口，下面接口使用的是fastapi框架:

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



2. 然后编辑你的自动化测试项目的conftest.py文件，增加`pytest_send_upload_request` 钩子:

```python
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_send_upload_request(upload_url, files, config):
    from pytest_upload_report.upload_client import SignUploadClient
    client = SignUploadClient(upload_url, files)
    client.send_request(config)
    return True
```

> hookimpl的装饰器加上tryfirst参数，可以确保先执行。
> 如果你不想别的pytest_send_upload_request钩子继续执行，钩子方法需返回True。
> 如果有多个地方都需要上传报告文件，请实现多个钩子，且钩子方法不需要任何返回值。


3. 最后编辑你的自动化测试项目的pytest.init文件，加上命令参数，免得pytest命令需要输入大量参数：

```buildoutcfg
[pytest]
addopts = --alluredir=/tmp/my_allure_results --upload_url=http://127.0.0.1:8000/api/script/reports/upload --upload_project_id=4 --upload_username=admin --upload_secret=8FB6CFB4C8CF11EBB523DCA9048E18C3
```


4. 在项目的根目录执行pytest后，查看上传结果吧：

```shell
$ pytest
```
    


> example目录是一个例子的源码，仅作参考。


### 自定义开发

如果上面的接口参数或者规则不满足你的需求，你可以自己写一个CustomUploadClient去实现上传逻辑。
