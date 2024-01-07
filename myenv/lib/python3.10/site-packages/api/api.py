#!/usr/bin/env python
import json
import pkg_resources
import platform
import sys
import re
import requests
from requests.auth import HTTPBasicAuth

class console:
    @staticmethod
    def error(text):
        print '\033[91m' + text + '\033[0m'
    @staticmethod
    def warn(text):
        print '\033[93m' + text + '\033[0m'

def config(key):
    return api(key)

class api():
    def __init__(self, key):
        self.key = key

    def __call__(self, service):
        request = Request(service=service, key=self.key)
        return request

class Request():
    def __init__(self, service, key):
        self.service = service
        self.key = key

    def run(self, method, data):
        split = re.search('(?:([-\w]+)/)?([-\w]+)(?:@([-.\w]+))?', self.service)
        organization = split.group(1)
        service = split.group(2)
        version_override = split.group(3)

        # Prefixes the organization (including an @) if there's an org
        # So, 'twitter/math' becomes '@twitter/math'
        service_full = '@%s/%s' % (organization, service) if organization else service

        headers = {
            'X-Build-Meta-Language': 'python@%s' % platform.python_version(),
            'X-Build-Meta-SDK': 'api@%s' % pkg_resources.require("api")[0].version,
            'X-Build-Meta-OS': '%s@%s' % (platform.system(), platform.release()),
        }

        if version_override:
            headers['X-Build-Version-Override'] = version_override

        out = requests.post('https://api.readme.build/v1/run/%s/%s' % (service_full, method),
            json=data,
            headers=headers,
            auth=HTTPBasicAuth(self.key, ''),
            verify=False # NO, bad! But issue with SSL certs
        )

        result = Response()

        try:
            content = out.json()
        except ValueError:
            content = out._content

        result.is_deprecated = (out.headers.setdefault('X-Build-Deprecated', 'false') == 'true')

        if result.is_deprecated:
            service = self.service
            version = out.headers['X-Build-Version']
            console.warn('%s v%s is deprecated! Run `api update %s` to use the latest version' % (
                service, version, service
            ))

        if out.status_code > 299:
            result.error = content
            content = None
            console.error(result.error['error'])

        return content, result

class Response():
    def __init__(self, error=None, is_deprecated=False):
        self.error = error
        self.is_deprecated = is_deprecated

