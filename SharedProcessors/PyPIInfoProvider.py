#!/usr/bin/env python
#
# Copyright 2014 Gerard Kok
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import xmlrpclib

from autopkglib import Processor, ProcessorError

__all__ = ["PyPIInfoProvider"]

class PyPIInfoProvider(Processor):
    """Provides URL and version to the latest update. Requires xmlrpclib."""
    description = __doc__
    input_variables = {
        "python_package": {
            "required": True,
            "description": "python package name",
        },
    }
    output_variables = {
        "url": {
            "description": "download url"
        },
        "version": {
            "description": "most recent version"
        }
    }


    def get_latest_version(self, client, package):
        versions = client.package_releases(package)
        if versions:
            version = versions[0]
            self.output("Found version: %s" % version)
            return version
        else:
            raise ProcessorError("No versions to be found.")


    def get_download_url(self, client, package, version):
        release_urls = client.release_urls(package, version)
        urls = [r["url"] for r in release_urls if r["packagetype"] == "sdist"]
        if urls:
            url = urls[0]
            self.output("Found url: %s" % url)
            return url
        else:
            raise ProcessorError("No download url found.")


    def main(self):
        package = self.env['python_package']
        client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
        version = self.get_latest_version(client, package)
        self.env["version"] = version
        self.env["url"] = self.get_download_url(client, package, version)

                
if __name__ == '__main__':
    processor = PyPIInfoProvider()
    processor.execute_shell()