#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path
import pytest


def pytest_addhooks(pluginmanager):
    from . import hooks
    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser):
    group = parser.getgroup('upload_report')
    group.addoption('--upload_url', action='store', dest='upload_url', default='')
    group.addoption('--upload_project_id', action='store', dest='upload_project_id', default='')
    group.addoption('--upload_secret', action='store', dest='upload_secret', default='')
    group.addoption('--upload_username', action='store', dest='upload_username', default='')


def pytest_configure(config):
    allure_plugin = config.pluginmanager.get_plugin("allure_pytest")
    if allure_plugin:
        report_dir = config.option.allure_report_dir
        if report_dir:
            import allure_commons
            from allure_pytest.plugin import cleanup_factory
            from .allure_upload import AllureFileUploadLogger
            from allure_commons.logger import AllureFileLogger

            # 卸载原有的AllureFileLogger插件，并还原cleanup
            plugin_list = []
            for plugin in allure_commons.plugin_manager.get_plugins():
                if isinstance(plugin, AllureFileLogger):
                    allure_commons.plugin_manager.unregister(plugin)
                    cleanup_list = []
                    for i, clean_item in enumerate(config._cleanup):
                        if clean_item.__module__ == 'allure_pytest.plugin' and clean_item.__name__ == 'clean_up':
                            continue
                        else:
                            cleanup_list.append(clean_item)
                    config._cleanup = cleanup_list
                else:
                    plugin_list.append(plugin)
            clean = config.option.clean_alluredir
            file_upload_logger = AllureFileUploadLogger(report_dir, clean)
            allure_commons.plugin_manager.register(file_upload_logger, 'allure_file_upload_logger')
            plugin_list.append(file_upload_logger)
            for plugin in plugin_list:
                config.add_cleanup(cleanup_factory(plugin))

    html_plugin = config.pluginmanager.get_plugin("html")
    if html_plugin:
        report_dir = config.option.htmlpath
        if report_dir:
            pass


def pytest_sessionfinish(session, exitstatus):
    allure_plugin = session.config.pluginmanager.get_plugin("allure_pytest")
    if allure_plugin:
        report_dir = session.config.option.allure_report_dir
        if report_dir:
            import allure_commons
            plugin = allure_commons.plugin_manager.get_plugin('allure_file_upload_logger')
            files = []
            for report_file in plugin.report_files:
                files.append(os.path.join(report_dir, report_file))
            session.config.hook.pytest_send_upload_request(
                upload_url=session.config.option.upload_url,
                files=files,
                config=session.config.option.__dict__,
            )

    html_plugin = session.config.pluginmanager.get_plugin("html")
    if html_plugin:
        report_dir = session.config.option.htmlpath
        if report_dir:
            pass


@pytest.hookimpl
def pytest_send_upload_request(upload_url, files, config):
    from .upload_client import UploadClient
    client = UploadClient(upload_url, files)
    client.send_request()
