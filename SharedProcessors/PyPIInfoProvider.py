#!/usr/local/autopkg/python
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

import json

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["PyPIInfoProvider"]

PYPI_SIMPLE_API = "https://pypi.org/pypi/{0}/json"

class PyPIInfoProvider(URLGetter):
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
            "description": "download url of most recent version"
        },
        "filename": {
            "description": "filename of most recent version"
        },
        "version": {
            "description": "most recent version"
        }
    }

    def get_filename(self, version_info):
        filenames = [r["filename"] for r in version_info if r["packagetype"] == "sdist"]
        if filenames:
            filename = filenames[0]
            self.output("Found filename: %s" % filename)
            return filename
        else:
            raise ProcessorError("No filename found.")


    def get_download_url(self, version_info):
        urls = [r["url"] for r in version_info if r["packagetype"] == "sdist"]
        if urls:
            url = urls[0]
            self.output("Found url: %s" % url)
            return url
        else:
            raise ProcessorError("No download url found.")


    def main(self):
        package = self.env['python_package']
        pypi_url = PYPI_SIMPLE_API.format(package)
        response = self.download(pypi_url)
        pypi_info = json.loads(response)
        version = pypi_info["info"]["version"]
        self.env["version"] = version
        self.env["url"] = self.get_download_url(pypi_info["releases"][version])
        self.env["filename"] = self.get_filename(pypi_info["releases"][version])

                
if __name__ == '__main__':
    processor = PyPIInfoProvider()
    processor.execute_shell()
